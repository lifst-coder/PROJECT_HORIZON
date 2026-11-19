"""
PROJECT HORIZON Simulation Engine
Monte Carlo scenario analysis for key technology and resource variables.
Informed by 2026 public data (IEA, IFR, TrendForce, company roadmaps).
"""
import numpy as np
import pandas as pd

def run_simulation(n_sims=1000, seed=42):
    np.random.seed(seed)
    years = [2030, 2035, 2040, 2050]
    results = []
    
    for sim in range(n_sims):
        growth = np.random.triangular(0.10, 0.15, 0.20)
        ai_share = np.random.triangular(0.30, 0.40, 0.50)
        robot_cagr = np.random.triangular(0.05, 0.07, 0.10)
        humanoid_dt = np.random.triangular(6, 9, 12)
        fusion_start = int(np.random.triangular(2032, 2035, 2045))
        smr_base = np.random.triangular(5, 20, 50)
        
        base_dc = 589  # TWh 2026 estimate
        for year in years:
            yrs = year - 2026
            dc_twh = base_dc * (1 + growth)**yrs
            # Cap AI share growth
            ai_share_y = min(0.65, ai_share + 0.015 * max(0, year - 2030))
            ai_twh = dc_twh * ai_share_y
            
            robot_stock = 5.08 * (1 + robot_cagr)**(year - 2025)
            
            # Humanoid with soft saturation (logistic-like)
            months = (year - 2025) * 12
            raw = 0.016 * (2 ** (months / humanoid_dt))
            # Soft cap around 10M annual by 2040-ish
            humanoid_annual = raw / (1 + raw / 10.0)   # millions
            
            fusion_flag = 1 if year >= fusion_start else 0
            smr_gw = smr_base * max(0.0, (year - 2030) / 5.0) if year >= 2030 else 0
            
            results.append({
                'sim': sim, 'year': year,
                'dc_electricity_twh': round(dc_twh, 1),
                'ai_electricity_twh': round(ai_twh, 1),
                'industrial_robot_stock_m': round(robot_stock, 2),
                'humanoid_annual_prod_m': round(humanoid_annual, 3),
                'fusion_online': fusion_flag,
                'smr_capacity_gw': round(smr_gw, 1)
            })
    return pd.DataFrame(results)

if __name__ == '__main__':
    df = run_simulation()
    summary = df.groupby('year')[['dc_electricity_twh', 'ai_electricity_twh', 
                                   'industrial_robot_stock_m', 'humanoid_annual_prod_m',
                                   'smr_capacity_gw']].median().round(2)
    print(summary)
    df.to_csv('06_SIMULATION_RESULTS.csv', index=False)
    print('Results written.')
