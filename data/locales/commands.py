from discord import Embed, EmbedField, Color, Button


back_button = {
    "en-US": Button(
        label="Back",
        emoji="<:back_arrow:940318470069960744>",
        row=4
    ),
    "fr-FR": Button(
        label="Retour",
        emoji="<:back_arrow:940318470069960744>",
        row=4
    ),
}

exit_button = {
    "en-US": Button(label="Exit"),
    "fr-FR": Button(label="Sortir")
}

missing_permission_embed = {
    "en-US": Embed(
        title="⛔ Missing permissions",
        description="You need to be an administrator to use this command!",
        color=Color.embed_background()
    ),
    "fr-FR": Embed(
        title="⛔ Permissions manquantes",
        description="Vous devez être administrateur pour utiliser cette commande !",
        color=Color.embed_background()
    )
}


config_loc = {
    "name": {
        "en-US": "config",
        "fr-FR": "config"
    },
    "description": {
        "en-US": "Admins only. Configure the bot for your server.",
        "fr-FR": "Admins uniquement. Configurer le bot pour votre serveur."
    },
    "embeds": {
        "main": {
            "en-US": Embed(
                title=":gear: Config Statys for your server",
                description="Select an option in the buttons bellow.",
                color=Color.embed_background()
            ),
            "fr-FR": Embed(
                title=":gear: Configurer Statys pour votre serveur",
                description="Sélectionnez une option dans les buttons ci-dessous.",
                color=Color.embed_background()
            )
        },
        "select_supporter": {
            "en-US": Embed(
                title="🎭 Select a role",
                description="**Select the role that will be given to the supporters.**",
                color=Color.embed_background()
            ),
            "fr-FR": Embed(
                title="🎭 Sélectionner un rôle",
                description="**Sélectionnez le rôle qui sera donné aux supporteurs.**",
                color=Color.embed_background()
            ),
            "warning": {
                "en-US": "\n\n⚠ Your server seems to have more roles than the menu can handle. Use `/set-supporter` instead if you don't see the role you want in the dropdown.",
                "fr-FR": "\n\n⚠ Votre serveur à l'air d'avoir plus de rôles que le menu ne peut supporter. Utiliser `/set-supporteur` si vous ne trouvez pas le rôle que vous voulez dans la sélection."
            }
        },
        "exclude_roles": {
            "en-US": Embed(
                title="❌ Exclude roles",
                description="**The satus of the members with the selected roles won't be checked.**\n\n*Note: If one of the selected roles is also the role given to supporters, the members will never lose this role after getting it.*"
            ),
            "fr-FR": Embed(
                title="❌ Exclure des rôles",
                description="**Le statut des membres avec les rôles sélectionnés ne sera pas vérifié.**\n\n*Note : Si un des rôles sélectionnés est aussi le rôle supporteur, les membres ne perdront jamais ce rôle après l'avoir obtenu.*"
            ),
            "warning": {
                "en-US": "\n\n⚠ Your server seems to have more roles than the menu can handle. Use `/add-excluded` and `/remove-excluded` instead if you don't see the role you want in the dropdown.",
                "fr-FR": "\n\n⚠ Votre serveur à l'air d'avoir plus de rôles que le menu ne peut supporter. Utiliser `/ajouter-exception` et `/enlever-exception` si vous ne trouvez pas le rôle que vous voulez dans la sélection."
            }
        }
    },
    "buttons": {
        "select_supporter": {
            "en-US": "Role",
            "fr-FR": "Rôle"
        },
        "exclude_roles": {
            "en-US": "Exclude",
            "fr-FR": "Exclure"
        }
    },
    "dropdowns": {
        "select_supporter": {
            "en-US": "Do not give a role",
            "fr-FR": "Ne pas donner de rôle"
        }
    }
}

set_supporter_loc = {
    "name": {
        "en-US": "set-supporter",
        "fr-FR": "set-supporteur"
    },
    "description": {
        "en-US": "Admins only. Set the supporter role for this server.",
        "fr-FR": "Admins uniquement. Définir le rôle supporter pour votre serveur."
    }
}