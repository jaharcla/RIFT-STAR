package dev.riftstar.companion.satsu;

import java.util.Comparator;
import java.util.function.Consumer;

import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.event.entity.player.AttackEntityEvent;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/**
 * Optional client-only JARVIS bridge.
 *
 * The stock sampler is conservative: it can detect Satsu-namespace armor and
 * ordinary Minecraft conditions, but it does NOT claim to know Palladium power,
 * nanite counts, weapon selection, or Satsu flight APIs.
 *
 * The existing JARVIS <-> Satsu integration can register a telemetryProvider to
 * replace the fallback sampler with verified measurements. No chat commands,
 * keybinds, abilities, or movement are issued by this bridge.
 */
@Mod.EventBusSubscriber(modid = "riftstar_companion", value = Dist.CLIENT,
        bus = Mod.EventBusSubscriber.Bus.FORGE)
public final class ForgeSuitClientBridge {

    @FunctionalInterface
    public interface TelemetryProvider {
        /** Return null to use conservative vanilla-compatible fallback observations. */
        SuitTelemetry sample(LocalPlayer player, long tick);
    }

    private static final SuitIntelligence INTELLIGENCE = new SuitIntelligence();
    private static volatile TelemetryProvider telemetryProvider;
    private static volatile Consumer<SuitAdvisory> voiceSink;
    private static LocalPlayer lastPlayer;
    private static long clientTick;
    private static boolean pendingAttack, priorDamage;

    private ForgeSuitClientBridge() { }

    /** Connect your existing Satsu bridge; call from the Minecraft client thread. */
    public static void setTelemetryProvider(TelemetryProvider provider) {
        telemetryProvider = provider;
    }

    /** Optional JARVIS TTS/event pipeline hook. Never called from a background thread. */
    public static void setVoiceSink(Consumer<SuitAdvisory> sink) {
        voiceSink = sink;
    }

    @SubscribeEvent
    public static void onAttack(AttackEntityEvent event) {
        if (event.getEntity() instanceof LocalPlayer player
                && player.level().isClientSide()) {
            pendingAttack = true;
        }
    }

    @SubscribeEvent
    public static void onClientTick(TickEvent.ClientTickEvent event) {
        if (event.phase != TickEvent.Phase.END) return;
        Minecraft mc = Minecraft.getInstance();
        LocalPlayer player = mc.player;
        if (player == null || mc.level == null) {
            INTELLIGENCE.reset();
            lastPlayer = null;
            pendingAttack = false;
            priorDamage = false;
            return;
        }
        if (lastPlayer != player) {
            INTELLIGENCE.reset();
            clientTick = 0;
            lastPlayer = player;
            pendingAttack = false;
            priorDamage = false;
        }
        clientTick++;

        SuitTelemetry sample = null;
        TelemetryProvider provider = telemetryProvider;
        if (provider != null) {
            try {
                sample = provider.sample(player, clientTick);
            } catch (RuntimeException ex) {
                // An optional provider cannot bring down the whole client.
                // Preserve safe degradation: never invent reactor data.
            }
        }
        if (sample == null) sample = sampleFallback(player, clientTick);
        var result = INTELLIGENCE.update(sample);

        // The stock HUD-free build only emits transient action-bar messages.
        // A single highest-priority message avoids text and audio overlap.
        result.advisories().stream().max(Comparator.comparing(SuitAdvisory::level))
                .ifPresent(advisory -> player.displayClientMessage(
                        Component.literal("JARVIS | " + advisory.text()), true));

        Consumer<SuitAdvisory> sink = voiceSink;
        if (sink != null) {
            for (SuitAdvisory advisory : result.advisories()) {
                try { sink.accept(advisory); }
                catch (RuntimeException ignored) { /* audio must never break the suit */ }
            }
        }
    }

    private static SuitTelemetry sampleFallback(LocalPlayer player, long tick) {
        boolean detected = false;
        for (ItemStack stack : player.getArmorSlots()) {
            if (stack.isEmpty()) continue;
            ResourceLocation id = BuiltInRegistries.ITEM.getKey(stack.getItem());
            if (id != null && id.getNamespace().toLowerCase(java.util.Locale.ROOT)
                    .contains("satsu")) {
                detected = true;
                break;
            }
        }
        // Only infer ordinary Minecraft flight flags, not Satsu-specific flight
        // mechanics. The native telemetryProvider should supply flight mode.
        boolean flying = player.getAbilities().flying || player.isFallFlying();
        boolean damageNow = player.hurtTime > 0;
        boolean combat = pendingAttack || (damageNow && !priorDamage);
        pendingAttack = false;
        priorDamage = damageNow;

        double maxHealth = player.getMaxHealth();
        double health = maxHealth > 0
                ? Math.max(0, Math.min(1, player.getHealth() / maxHealth)) : 1;
        int hostiles = player.level()
                .getEntitiesOfClass(Monster.class, player.getBoundingBox().inflate(18),
                        mob -> mob.isAlive() && mob.hasLineOfSight(player)).size();

        return new SuitTelemetry(tick, detected, flying, combat, health,
                null /* no verified reactor telemetry */, hostiles,
                flying && flightObstacleAhead(player));
    }

    /** Vanilla block raycast along actual velocity. Not a Satsu physics override. */
    private static boolean flightObstacleAhead(LocalPlayer player) {
        Vec3 velocity = player.getDeltaMovement();
        if (velocity.lengthSqr() < 0.09) return false; // avoid idle false alarms
        Vec3 start = player.getEyePosition();
        Vec3 end = start.add(velocity.normalize().scale(8.0));
        return player.level().clip(new ClipContext(start, end,
                ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, player))
                .getType() == HitResult.Type.BLOCK;
    }
}
