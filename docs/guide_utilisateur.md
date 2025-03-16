# Guide Utilisateur

<div align="center">
  
![Chatbot-RAG](https://img.shields.io/badge/Chatbot-RAG-blue?style=for-the-badge&logo=robot&logoColor=white)

**Assistant Juridique sur la Protection des Données Personnelles au Sénégal**

*Votre guide pour une expérience optimale avec notre assistant conversationnel juridique*

</div>

## Table des Matières

1. [Introduction](#introduction)
2. [Premiers Pas](#premiers-pas)
3. [Poser des Questions](#poser-des-questions)
4. [Comprendre les Réponses](#comprendre-les-réponses)
5. [Fonctionnalités Avancées](#fonctionnalités-avancées)
6. [Résolution des Problèmes](#résolution-des-problèmes)
7. [Foire Aux Questions](#foire-aux-questions)

## Introduction

Bienvenue dans le guide utilisateur du **Chatbot-RAG**, un assistant conversationnel spécialisé dans la législation sénégalaise sur la protection des données personnelles (Loi n° 2008-12 du 25 janvier 2008). Cet outil a été conçu pour vous fournir des informations précises et contextuelles sur cette loi, en vous offrant une expérience conversationnelle intuitive et enrichissante.

Notre chatbot utilise une technologie de pointe combinant la recherche sémantique et l'intelligence artificielle générative (RAG - Retrieval-Augmented Generation) pour vous fournir des réponses fondées sur le texte exact de la loi, avec des références précises aux articles pertinents.

## Premiers Pas

### Accéder à l'Interface

1. Ouvrez votre navigateur web préféré
2. Accédez à l'URL fournie par votre administrateur système (généralement `http://localhost:7860` en environnement local)
3. L'interface du chatbot se charge automatiquement et est immédiatement prête à répondre à vos questions

### Comprendre l'Interface

L'interface du Chatbot-RAG est intuitive et comprend les éléments suivants :

- **Zone de conversation** : Affiche l'historique de vos échanges avec le chatbot
- **Zone de saisie** : Permet d'entrer vos questions
- **Bouton d'envoi** : Pour soumettre votre question
- **Bouton de réinitialisation** : Pour démarrer une nouvelle conversation
- **Section d'exemples** : Propose des questions prédéfinies pour vous aider à démarrer
- **Options d'export** : Pour télécharger votre conversation au format Markdown ou texte
- **Section "À propos"** : Fournit des informations supplémentaires sur le chatbot

### Changer le Thème (Clair/Sombre)

Vous pouvez basculer entre le mode clair et le mode sombre en utilisant le bouton de paramètres situé en bas à droite de l'interface.

## Poser des Questions

### Conseils pour des Questions Efficaces

Pour obtenir les meilleures réponses possibles :

- **Soyez précis** : "Quelles sont les missions de la CDP ?" est préférable à "Parlez-moi de la CDP"
- **Posez une question à la fois** : Évitez de combiner plusieurs questions dans un même message
- **Utilisez des termes juridiques** : Si vous connaissez les termes exacts (CDP, données sensibles, etc.), utilisez-les
- **Précisez le contexte** : Si votre question concerne un aspect spécifique, mentionnez-le

### Exemples de Questions Pertinentes

- "Qu'est-ce que la Commission des Données Personnelles (CDP) et quelles sont ses missions ?"
- "Quels sont les droits des personnes concernées par un traitement de données personnelles ?"
- "Dans quels cas peut-on transférer des données personnelles vers un pays tiers ?"
- "Comment sont sanctionnés les manquements à la loi sur la protection des données ?"
- "Quelles sont les formalités préalables à la mise en œuvre d'un traitement de données ?"
- "Comment est définie une donnée à caractère personnel selon la loi sénégalaise ?"

## Comprendre les Réponses

### Structure des Réponses

Chaque réponse du chatbot est structurée de manière à faciliter votre compréhension :

1. **Réponse directe** à votre question, formulée de manière claire et concise
2. **Citations des articles pertinents** de la loi, avec leur numéro
3. **Explications complémentaires** sur les implications pratiques si nécessaire
4. **Sources utilisées** listées à la fin de la réponse, avec le chapitre, la section et l'article correspondants

### Interprétation des Sources

À la fin de chaque réponse, vous trouverez une section "Sources utilisées" qui indique :

- Le chapitre et la section de la loi
- Le numéro de l'article cité
- Un score de similarité (%) indiquant la pertinence de la source

Plus le score est élevé, plus la source est considérée comme pertinente pour votre question.

## Fonctionnalités Avancées

### Exporter vos Conversations

Vous pouvez sauvegarder l'intégralité de votre conversation pour référence ultérieure :

1. Cliquez sur la section "Options d'export" pour la déplier
2. Choisissez le format souhaité (Markdown ou Texte)
3. Cliquez sur "📥 Télécharger la conversation"
4. Un fichier sera généré et proposé au téléchargement

### Utiliser les Exemples Prédéfinis

En bas de l'interface, vous trouverez des exemples de questions. En cliquant sur l'un d'entre eux, la question sera automatiquement insérée dans la zone de saisie, prête à être envoyée.

### Copier des Portions de Réponse

Vous pouvez facilement copier une partie spécifique d'une réponse en la sélectionnant puis en utilisant le raccourci clavier Ctrl+C (ou Cmd+C sur Mac).

## Résolution des Problèmes

### Réponses Génériques ou Hors Sujet

Si vous recevez une réponse qui semble générique ou hors sujet :

- Reformulez votre question en étant plus précis
- Utilisez des termes juridiques exacts si vous les connaissez
- Vérifiez que votre question concerne bien la loi sénégalaise sur la protection des données personnelles

### Problèmes de Connexion

Si vous voyez un message d'erreur concernant l'API :

1. Vérifiez votre connexion internet
2. Assurez-vous que le serveur API est en cours d'exécution (contactez votre administrateur système)
3. Rechargez la page et réessayez après quelques instants

### Réinitialisation de la Conversation

Si vous rencontrez des comportements étranges ou souhaitez simplement repartir à zéro :

1. Cliquez sur le bouton "🔄 Nouvelle conversation"
2. La conversation sera entièrement réinitialisée

## Foire Aux Questions

**Q : Le chatbot peut-il répondre à des questions sur d'autres lois ?**  
R : Non, ce chatbot est spécialisé uniquement dans la loi sénégalaise sur la protection des données personnelles (Loi n° 2008-12 du 25 janvier 2008).

**Q : Les réponses fournies ont-elles une valeur juridique ?**  
R : Non, les réponses fournies sont à titre informatif uniquement et ne constituent pas un avis juridique professionnel. Pour des conseils juridiques, veuillez consulter un avocat.

**Q : Comment le chatbot trouve-t-il ses réponses ?**  
R : Le chatbot utilise l'approche RAG (Retrieval-Augmented Generation) qui consiste à rechercher les passages pertinents dans la loi puis à générer une réponse basée sur ces extraits spécifiques.

**Q : Puis-je suggérer des améliorations au chatbot ?**  
R : Oui, n'hésitez pas à contacter l'équipe de développement pour partager vos retours et suggestions d'amélioration.

**Q : Les conversations sont-elles enregistrées ou partagées ?**  
R : Les conversations ne sont pas enregistrées sur le serveur une fois votre session terminée, sauf si vous les exportez vous-même.

---

<div align="center">
  <p>Nous espérons que ce guide vous aidera à tirer le meilleur parti de notre assistant juridique.</p>
  <p>Pour toute question ou assistance supplémentaire, n'hésitez pas à contacter notre équipe.</p>
</div>