screen JK_ToggleSettingGlobalizationButton(key, disabled=False, force_enabled=False):
    if JK.UserDir.is_available():
        $ enabled = force_enabled or key in JK.Settings.globalizedSettings

        hbox yalign 0.5:
            use JK_IconButton(icon="\ue80b" if enabled else "\uf1ca", action=JK.Settings.ToggleGlobalizedSettingAction(key), color=JK.Colors.success if enabled else JK.Colors.text_light, size=20, tt="Disable globalization of this setting" if enabled else "Enable globalization for this setting.\nIf enabled, this setting's value will be shared across all games.\nCurrently {color=[JK.Colors.error]}disabled{/color}.", disabled=disabled, hover_color=JK.Colors.hover, disabled_color=JK.Colors.status_enabled_disabled if enabled else JK.Colors.disabled)