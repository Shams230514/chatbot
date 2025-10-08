#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BNDE CHATBOT - Version Optimisée avec Formatage Amélioré
Assistant virtuel limité à la base de connaissances BNDE
"""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import Dict, Any
import base64
import re

# Message de garde-fou
HORS_SUJET = "Désolé je suis un assistant virtuel de la BNDE, ma connaissance se limite aux produits et services de la BNDE"

# Base de connaissances complète intégrée
BNDE_KNOWLEDGE = """
PRÉSENTATION DE LA BNDE

La Banque Nationale pour le Développement Économique (BNDE) a démarré ses activités en janvier 2014. C'est une banque à vocation universelle dédiée particulièrement aux PME-PMI, fonctionnant selon un modèle de partenariat Public-Privé.

Mission de la BNDE : Contribuer à créer et développer des entreprises sénégalaises en offrant des produits et services diversifiés et adaptés, avec une attention particulière sur les PME-PMI.

Objectifs spécifiques :
- Accompagner la croissance des PME-PMI (création, restructuration, expansion)
- Contribuer au développement économique et social du Sénégal
- Financer les besoins des acteurs économiques au-delà des PME
- Financer le secteur productif moderne et le secteur informel à forte valeur ajoutée

PRODUITS ET SERVICES BNDE :
- COMPTES BANCAIRES
- PACKAGES
- MONÉTIQUE
- BANQUE DIGITALE
- PLACEMENT ET ÉPARGNE
- FINANCEMENT
- BANCASSURANCE

COMPTE COURANT
- Définition : Compte de dépôt à vue pour opérations bancaires courantes
- Clientèle : Particuliers, Entreprises, Professionnels
- Frais : 2 925 FCFA TTC

COMPTE ÉPARGNE
- Pour : Personnes physiques de 30 ans et plus
- Taux : 3,5% l'an (net d'impôts)
- Solde max rémunéré : 6 000 000 FCFA
- Frais : Gratuit

DOCUMENTS - COMPTE COURANT PARTICULIERS :
- Photocopie CNI ou passeport
- 2 photos d'identité
- Certificat de résidence OU quittance eau/électricité/téléphone

DOCUMENTS - COMPTE COURANT ENTREPRISE :
- Certificat inscription registre de commerce
- Carte d'identité
- Certificat de résidence OU quittance
- 2 photos
- Certificat immatriculation fichier contribuables

DOCUMENTS - COMPTE COURANT SARL :
- Certificat inscription registre de commerce
- Certificat immatriculation contribuables
- Annonces légales
- Pouvoirs personnes habilitées
- Cartes identité et photos
- Certificat résidence OU quittance
- Dernier bilan (facultatif)

DOCUMENTS - COMPTE ÉPARGNE :
- 3 photos d'identité
- Certificat domicile OU quittance
- Photocopie CNI ou passeport

PACKAGES PARTICULIERS (NAFIO) : Ganalé, Kilifa, Wurus
PACKAGES ENTREPRISES (TERRU) : DOOLEL, YAATAL, NDARIN, AND JAPPO
"""

# Mots-clés BNDE
BNDE_KEYWORDS = [
    'bnde', 'banque', 'compte', 'épargne', 'courant', 'ouvrir', 'ouverture',
    'document', 'pièce', 'frais', 'taux', 'package', 'nafio', 'terru',
    'particulier', 'entreprise', 'service', 'produit', 'carte', 'crédit'
]

def get_logo():
    """Logo BNDE SVG"""
    svg = """
    <svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#1e3a8a;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect width="60" height="60" rx="12" fill="url(#grad)"/>
        <text x="30" y="38" font-family="Arial" font-size="28" font-weight="800" 
              fill="white" text-anchor="middle">B</text>
    </svg>
    """
    return base64.b64encode(svg.encode()).decode()

def format_response(text: str) -> str:
    """Formate la réponse pour une meilleure lisibilité"""
    # Si c'est le message hors sujet, on le retourne tel quel
    if HORS_SUJET in text:
        return text
    
    # Remplacer les tirets par des puces avec saut de ligne
    text = re.sub(r'\s*-\s*', '\n• ', text)
    
    # Ajouter des sauts de ligne après les deux-points suivis de texte
    text = re.sub(r':\s*([A-Z•])', r':\n\n\1', text)
    
    # Nettoyer les multiples sauts de ligne
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

st.set_page_config(page_title="Leuk", page_icon="🏦", layout="centered")

# CSS Optimisé
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
* { font-family: 'Inter', sans-serif !important; }

.main .block-container { padding: 1.5rem !important; max-width: 800px !important; }

.header {
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    padding: 1.5rem;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 20px rgba(30, 58, 138, 0.25);
}

.header h1 {
    color: white;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0;
}

.header p {
    color: rgba(255,255,255,0.9);
    font-size: 0.9rem;
    margin: 0.5rem 0 0 0;
}

.user-msg {
    background: #eff6ff;
    padding: 1rem;
    border-radius: 12px;
    margin: 0.8rem 0;
    border-left: 3px solid #3b82f6;
}

.ai-msg {
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    color: white;
    padding: 1.2rem;
    border-radius: 12px;
    margin: 0.8rem 0;
    line-height: 1.8;
    white-space: pre-line;
}

.warning-msg {
    background: #fef3c7;
    color: #92400e;
    padding: 1rem;
    border-radius: 12px;
    margin: 0.8rem 0;
    border-left: 3px solid #f59e0b;
    font-weight: 500;
}

.stButton > button {
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    width: 100%;
    transition: transform 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(30, 58, 138, 0.3);
}

.quick-btn {
    background: #eff6ff;
    border: 1px solid #3b82f6;
    color: #1e3a8a;
    padding: 0.6rem;
    border-radius: 8px;
    margin: 0.3rem;
    cursor: pointer;
    font-size: 0.85rem;
    transition: all 0.2s;
}

.quick-btn:hover {
    background: #3b82f6;
    color: white;
    transform: translateY(-1px);
}
</style>
""", unsafe_allow_html=True)

# Configuration API
OPENWEBUI_BASE_URL = "https://accelchatbot-chatbotaccel.apps.senum.heritage.africa"
API_KEY = 'sk-3ae1aa4cf637456b8a8b958b86f1ea4c'

def is_bnde_question(text: str) -> bool:
    """Vérifie si la question concerne la BNDE"""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in BNDE_KEYWORDS)

def ask_bnde(question: str) -> Dict[str, Any]:
    """Interroge l'API avec la base BNDE"""
    
    # Filtre pré-IA
    if not is_bnde_question(question):
        return {"success": True, "response": HORS_SUJET, "filtered": True}
    
    # Prompt court et direct avec instruction de formatage
    system_msg = f"""Tu es l'assistant BNDE. Réponds UNIQUEMENT avec les informations ci-dessous.
Si l'info n'est pas dans cette base, dis: "{HORS_SUJET}"

IMPORTANT : Pour les listes de documents, présente-les avec des tirets sur des lignes séparées pour une meilleure lisibilité.

{BNDE_KNOWLEDGE}

Question: {question}
Réponds de façon claire et structurée."""
    
    try:
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "model": "mistral:7b",
            "messages": [{"role": "user", "content": system_msg}],
            "stream": False,
            "temperature": 0.1,
            "max_tokens": 800
        }
        
        response = requests.post(
            f"{OPENWEBUI_BASE_URL}/api/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                answer = data['choices'][0]['message']['content']
                # Formatage de la réponse
                formatted_answer = format_response(answer)
                return {"success": True, "response": formatted_answer, "filtered": False}
        
        return {"success": False, "response": "Erreur de connexion. Réessayez."}
        
    except Exception as e:
        return {"success": False, "response": "Erreur technique. Réessayez."}

# Header
st.markdown(f"""
<div class="header">
    <h1>Leuk</h1>
    <h1>Assistant Virtuel BNDE</h1>
    <p>Banque Nationale pour le Développement Économique</p>
</div>
""", unsafe_allow_html=True)

# Initialisation
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# Affichage historique
for msg in st.session_state.messages:
    if msg['role'] == 'user':
        st.markdown(f'<div class="user-msg"><strong>Vous :</strong> {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        css_class = "warning-msg" if msg.get('filtered') else "ai-msg"
        st.markdown(f'<div class="{css_class}"><strong>Leuk :</strong> {msg["content"]}</div>', unsafe_allow_html=True)

# Zone de saisie avec key dynamique pour reset
user_input = st.text_input(
    "Votre question",
    placeholder="Ex: Qui est la BNDE ? Quels documents pour ouvrir un compte ?",
    key=f"input_{st.session_state.input_key}",
    label_visibility="collapsed"
)

col1, col2 = st.columns([3, 1])
with col1:
    send = st.button("Envoyer", type="primary", use_container_width=True)
with col2:
    clear = st.button("Effacer", use_container_width=True)

# Traitement
if send and user_input.strip():
    # Ajout question
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    
    # Réponse
    with st.spinner("Leuk réfléchit..."):
        result = ask_bnde(user_input)
        if result['success']:
            st.session_state.messages.append({
                'role': 'assistant',
                'content': result['response'],
                'filtered': result.get('filtered', False)
            })
    
    # Reset input
    st.session_state.input_key += 1
    st.rerun()

if clear:
    st.session_state.messages = []
    st.session_state.input_key += 1
    st.rerun()

# Questions rapides
st.markdown("---")
st.markdown("**Questions fréquentes**")

col1, col2, col3 = st.columns(3)

questions_rapides = [
    ("Qui est la BNDE ?", col1),
    ("Quel est le taux d'épargne ?", col2),
    ("Quels documents pour un compte ?", col3)
]

for question, col in questions_rapides:
    with col:
        if st.button(question, key=f"q_{hash(question)}", use_container_width=True):
            # Ajout question
            st.session_state.messages.append({'role': 'user', 'content': question})
            
            # Réponse immédiate
            with st.spinner(""):
                result = ask_bnde(question)
                if result['success']:
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': result['response'],
                        'filtered': result.get('filtered', False)
                    })
            
            st.rerun()

# Info
with st.expander("À propos"):
    st.info("""
    **Assistant BNDE**
    
    Je réponds uniquement aux questions sur :
    - Les comptes bancaires (courant, épargne)
    - Les documents requis
    - Les packages (NAFIO, TERRU)
    - Les tarifs et conditions
    
    Pour toute autre question supplémentaire, contactez directement la banque.
    """)