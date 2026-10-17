from pathlib import Path
import os
import re
import subprocess
import shutil
import zipfile

here = Path(__file__).resolve().parent
root = here.parent
properties = {}
for line in (here / 'gradle.properties').read_text(encoding='utf-8').splitlines():
    if line and not line.startswith('#') and '=' in line:
        key, value = line.split('=', 1)
        properties[key.strip()] = value.strip()

java_home = Path(os.environ['JAVA_HOME']) if os.environ.get('JAVA_HOME') else None
if java_home:
    javac = java_home / 'bin' / ('javac.exe' if os.name == 'nt' else 'javac')
else:
    javac = Path(shutil.which('javac') or '')
if not javac.is_file():
    raise SystemExit('Java 17 javac is required; set JAVA_HOME or add javac to PATH')
version = subprocess.run([str(javac), '-version'], capture_output=True, text=True, check=True)
version_text = version.stderr or version.stdout
if not re.search(r'\b17(?:\.\d+)?(?:\D|$)', version_text):
    raise SystemExit(f'Java 17 is required, found: {version_text.strip()}')
forge = properties['forge_version']
mc = properties['minecraft_version']
fml = root / 'server' / 'libraries' / 'net' / 'minecraftforge' / 'javafmllanguage' / f'{mc}-{forge}' / f'javafmllanguage-{mc}-{forge}.jar'
if not fml.is_file():
    raise SystemExit(f'Missing Forge library: {fml}')

classes = here / 'build' / 'local-classes'
classes.mkdir(parents=True, exist_ok=True)
sources = sorted((here / 'src' / 'main' / 'java').rglob('*.java'))
subprocess.run([str(javac), '--release', '17', '-cp', str(fml), '-d', str(classes), *map(str, sources)], check=True)

output = here / 'build' / 'libs' / f"{properties['mod_id']}-{properties['mod_version']}.jar"
output.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as jar:
    for source in classes.rglob('*'):
        if source.is_file():
            jar.write(source, source.relative_to(classes).as_posix())
    resources = here / 'src' / 'main' / 'resources'
    for source in resources.rglob('*'):
        if source.is_file():
            content = source.read_bytes()
            if source.suffix in ('.toml', '.mcmeta'):
                rendered = content.decode('utf-8')
                rendered = re.sub(r'\$\{([^}]+)\}', lambda match: properties[match.group(1)], rendered)
                content = rendered.encode('utf-8')
            jar.writestr(source.relative_to(resources).as_posix(), content)
print(output)
