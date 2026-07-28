"""Generates professional static charts using Seaborn and Matplotlib."""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.logger import get_logger

logger = get_logger()

class ChartGenerator:
    def __init__(self, df: pd.DataFrame, output_dir: str):
        self.df = df
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set professional aesthetic
        sns.set_theme(style="whitegrid", palette="muted")
        plt.rcParams.update({'figure.autolayout': True})

    def generate_all(self):
        if self.df.empty:
            logger.error("Empty DataFrame. Cannot generate charts.")
            return
            
        self._plot_auth_distribution()
        self._plot_buildability()
        self._plot_category_mcp()
        logger.info(f"Charts saved to {self.output_dir}")

    def _plot_auth_distribution(self):
        plt.figure(figsize=(10, 6))
        ax = sns.countplot(data=self.df, y='auth_primary', order=self.df['auth_primary'].value_counts().index)
        plt.title('Authentication Method Distribution across 100 SaaS Apps', fontsize=14, pad=15)
        plt.xlabel('Number of Applications')
        plt.ylabel('Primary Auth Method')
        plt.savefig(os.path.join(self.output_dir, 'auth_distribution.png'), dpi=300, bbox_inches='tight')
        plt.close()

    def _plot_buildability(self):
        plt.figure(figsize=(8, 8))
        data = self.df['buildability'].value_counts()
        plt.pie(data.values, labels=data.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
        plt.title('Buildability Assessment', fontsize=14, pad=15)
        plt.savefig(os.path.join(self.output_dir, 'buildability_pie.png'), dpi=300, bbox_inches='tight')
        plt.close()

    def _plot_category_mcp(self):
        plt.figure(figsize=(12, 8))
        crosstab = pd.crosstab(self.df['category'], self.df['mcp_support'])
        sns.heatmap(crosstab, annot=True, fmt='d', cmap='Blues')
        plt.title('MCP Adoption by Category', fontsize=14, pad=15)
        plt.ylabel('Application Category')
        plt.xlabel('MCP Support Status')
        plt.savefig(os.path.join(self.output_dir, 'category_mcp_heatmap.png'), dpi=300, bbox_inches='tight')
        plt.close()
