import pandas as pd
from datetime import datetime
from typing import List, Dict

def calculate_urgent_deals(csv_path: str) -> List[Dict[str, float]]:
    # 1) Charger le CSV
    df = pd.read_csv(csv_path)
    
    # 2) Nettoyer et convertir amount_eur en float
    #    ex: "45 000" → "45000" → 45000.0
    df['amount_eur'] = (
        df['amount_eur']
        .astype(str)
        .str.replace(' ', '', regex=False)
        .astype(float)
    )
    
    # 3) Convertir last_activity en datetime et calcul idle_days
    df['last_activity'] = pd.to_datetime(df['last_activity'], utc=True)
    now = datetime.now(tz=df['last_activity'].dt.tz)
    df['idle_days'] = (now - df['last_activity']).dt.days
    
    # 4) Calculer l'urgence en milliers d'euros (30 au lieu de 30000)
    df['urgency'] = df['idle_days'] * (df['amount_eur'] / 1000)
    
    # 5) Filtrer les urgences > 250
    urgent_df = df[df['urgency'] > 250]
    
    # 6) Retourner la liste de dictionnaires
    return urgent_df[['deal_id', 'urgency']].to_dict(orient='records')


# Exemple d'utilisation
if __name__ == "__main__":
    result = calculate_urgent_deals("data/crm_events.csv")
    print("Deals with urgency > 250:")
    for item in result:
        print(f"  • {item['deal_id']}: urgency = {item['urgency']:.2f}")
