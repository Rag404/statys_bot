from discord import Embed, Color, EmbedField, Button, ButtonStyle


buttons = {
    "back_button": Button(
        label="Retour",
        emoji="<:back_arrow:940318470069960744>"
    ),
    
    "exit_button": Button(
        label="Sortir",
        style=ButtonStyle.red
    )
}


commands = {
    "config": {
        "name": "config",
        "description": "Admins uniquement. Configurer le bot pour votre serveur."
    },
    
    "set_supporter": {
        "name": "set-supporteur",
        "description": "Admins uniquement. Définir le rôle supporter pour votre serveur.",
        "options": {
            "role": {
                "name": "rôle",
                "description": "Sélectionner un rôle"
            }
        }
    },

    "add_excluded": {
        "name": "ajouter-exception",
        "description": "Admins uniquement. Ajouter un rôle dans la liste des exceptions.",
        "options": {
            "role": {
                "name": "rôle",
                "description": "Sélectionner un rôle"
            }
        }
    },

    "remove_excluded": {
        "name": "enlever-exceptions",
        "description":"Admins uniquement. Enlever un rôle de la liste des exceptions.",
        "options": {
            "name": "rôle",
            "description": "Sélectionner un rôle"
        }
    },

    "help": {
        "name": "help",
        "description": "Affiche le Menu d'Aide"
    },

    "infos": {
        "name": "infos",
        "description": "Affiche des informations sur le bot."
    },

    "feedback": {
        "name": "feedback",
        "description": "Signaler un bug, proposer une fonctionnalité ou envoyer un commentaire.",
        "modal": {

        }
    },

    "server-infos": {
        "name": "infos-serveur",
        "description": "Affiche des informations à propos de ce serveur.",
        "embeds": {
            "main_embed": Embed(
                title="ℹ Infos sur ce serveur",
                color=Color.embed_background(),
                fields=[
                    EmbedField(
                        name="- Nombre de supporteurs",
                        value="{supporters_text}"
                    ),
                    EmbedField(
                        name="- Rôle supporteur",
                        value="{supporter_role_text}"
                    ),
                    EmbedField(
                        name="- Exceptions",
                        value="{excluded_roles_text}",
                        inline=False
                    )
                ]
            ),
            "data_embed": Embed(
                title="📂 Données collectées",
                description="J'ai besoins de de collecter certaines données sur votre serveur pour bien fonctionner. Mais ne vous inquiétez pas, ce ne sont pas des données sensibles !\nJe collecte seulement les ID du **rôle supporteur** et des **rôles d'exception** de chaque serveur",
                color=Color.embed_background(),
                fields=[
                    EmbedField(
                        name="Les données de votre serveur",
                        value="```json\n{data}\n```"
                    )
                ]
            )
        },
        "buttons": {
            "to_data_button": Button(
                label="Données collectées",
                emoji="📂"
            ),
            "back_button": buttons["back_button"],
            "exit_button": buttons["exit_button"]
        }
    }
}