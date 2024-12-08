screen SSSSS_ToggleSettingGlobalizationButton(key, disabled=False, force_enabled=False):
    $ enabled = force_enabled or key in SSSSS.Settings.globalizedSettings

    hbox yalign 0.5:
        use sssss_iconButton(icon="\ue80b" if enabled else "\uf1ca", action=SSSSS.Settings.ToggleGlobalizedSetting(key), color=SSSSS.Colors.success if enabled else SSSSS.Colors.text_light, size=20, tt="Disable globalization of this setting" if enabled else "Enable globalization for this setting.\nIf enabled, this setting's value will be shared across all games.\nCurrently {color=[SSSSS.Colors.error]}disabled{/color}.", disabled=disabled, hover_color=SSSSS.Colors.hover, disabled_color=SSSSS.Colors.status_enabled_disabled)