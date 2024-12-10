screen URPS_ToggleSettingGlobalizationButton(key, disabled=False, force_enabled=False):
    if URPS.UserDir.is_available():
        $ enabled = force_enabled or key in URPS.Settings.globalizedSettings

        hbox yalign 0.5:
            use URPS_IconButton(icon="\ue80b" if enabled else "\uf1ca", action=URPS.Settings.ToggleGlobalizedSetting(key), color=URPS.Colors.success if enabled else URPS.Colors.text_light, size=20, tt="Disable globalization of this setting" if enabled else "Enable globalization for this setting.\nIf enabled, this setting's value will be shared across all games.\nCurrently {color=[URPS.Colors.error]}disabled{/color}.", disabled=disabled, hover_color=URPS.Colors.hover, disabled_color=URPS.Colors.status_enabled_disabled)