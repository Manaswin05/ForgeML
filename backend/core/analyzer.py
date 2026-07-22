import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from sklearn.model_selection import cross_validate
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

class DatasetAnalyzer:
    @staticmethod
    def _df_to_base64_image(fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        plt.close(fig)
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode('utf-8')

    @staticmethod
    def get_correlation_matrix(df, cols):
        numeric_cols = df[cols].select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return None
        
        corr = df[numeric_cols].corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title('Correlation Matrix')
        return DatasetAnalyzer._df_to_base64_image(plt.gcf())

    @staticmethod
    def get_pairplot(df, feature_cols, target_col):
        cols_to_plot = list(feature_cols)
        # Limit to 5 features for pairplot to avoid huge images and long compute
        if len(cols_to_plot) > 5:
            cols_to_plot = cols_to_plot[:5]
            
        plot_cols = cols_to_plot + [target_col]
        # Drop rows with NaNs in these columns for seaborn
        plot_df = df[plot_cols].dropna()
        
        if plot_df.empty:
            return None
        
        # Subsample if too large
        if len(plot_df) > 1000:
            plot_df = plot_df.sample(1000, random_state=42)
            
        is_target_categorical = plot_df[target_col].dtype == 'object' or len(plot_df[target_col].unique()) < 10
        
        if is_target_categorical:
            g = sns.pairplot(plot_df, hue=target_col, diag_kind='kde')
        else:
            g = sns.pairplot(plot_df, diag_kind='kde')
            
        return DatasetAnalyzer._df_to_base64_image(g.fig)
        
    @staticmethod
    def get_boxplots(df, feature_cols, target_col):
        numeric_features = df[feature_cols].select_dtypes(include=[np.number]).columns
        if len(numeric_features) == 0:
            return None
            
        is_target_categorical = df[target_col].dtype == 'object' or len(df[target_col].unique()) < 10
        
        num_plots = min(len(numeric_features), 6) # max 6 boxplots
        features_to_plot = numeric_features[:num_plots]
        
        cols = 2
        rows = (num_plots + 1) // 2
        
        fig, axes = plt.subplots(rows, cols, figsize=(12, 4 * rows))
        axes = axes.flatten()
        
        for i, col in enumerate(features_to_plot):
            if is_target_categorical:
                sns.boxplot(x=target_col, y=col, data=df, ax=axes[i])
            else:
                sns.scatterplot(x=target_col, y=col, data=df, ax=axes[i], alpha=0.5)
                
        # Hide empty subplots
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])
            
        plt.tight_layout()
        return DatasetAnalyzer._df_to_base64_image(fig)

    @staticmethod
    def compare_models(df, feature_cols, target_col):
        # Prepare data
        X = df[feature_cols]
        y = df[target_col]
        
        # Handle categoricals basically
        X = pd.get_dummies(X, drop_first=True)
        
        is_classification = y.dtype == 'object' or len(y.unique()) < 10
        
        # Fill missing values and scale
        imputer = SimpleImputer(strategy='median')
        try:
            X_imputed = imputer.fit_transform(X)
        except:
            X_imputed = X.fillna(0)
            
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_imputed)
        
        # Limit rows for speed
        if len(X_scaled) > 2000:
            indices = np.random.choice(len(X_scaled), 2000, replace=False)
            X_scaled = X_scaled[indices]
            y = y.iloc[indices]
            
        results = []
        if is_classification:
            # Classification
            if y.dtype == 'object' or y.dtype.name == 'category':
                from sklearn.preprocessing import LabelEncoder
                y = LabelEncoder().fit_transform(y)
                
            models = {
                'Logistic Regression': LogisticRegression(max_iter=1000),
                'Random Forest': RandomForestClassifier(n_estimators=50, random_state=42),
                'SVM': SVC(probability=True)
            }
            scoring = ['accuracy', 'f1_macro']
            
            for name, model in models.items():
                try:
                    cv_results = cross_validate(model, X_scaled, y, cv=3, scoring=scoring)
                    results.append({
                        'model': name,
                        'metric1_name': 'Accuracy',
                        'metric1_value': f"{cv_results['test_accuracy'].mean():.4f}",
                        'metric2_name': 'F1 Score',
                        'metric2_value': f"{cv_results['test_f1_macro'].mean():.4f}"
                    })
                except Exception as e:
                    print(f"Error training {name}: {e}")
                    pass
        else:
            # Regression
            models = {
                'Linear Regression': LinearRegression(),
                'Random Forest': RandomForestRegressor(n_estimators=50, random_state=42),
                'SVR': SVR()
            }
            scoring = ['neg_mean_squared_error', 'r2']
            
            for name, model in models.items():
                try:
                    cv_results = cross_validate(model, X_scaled, y, cv=3, scoring=scoring)
                    rmse = np.sqrt(-cv_results['test_neg_mean_squared_error'].mean())
                    results.append({
                        'model': name,
                        'metric1_name': 'RMSE',
                        'metric1_value': f"{rmse:.4f}",
                        'metric2_name': 'R2 Score',
                        'metric2_value': f"{cv_results['test_r2'].mean():.4f}"
                    })
                except Exception as e:
                    print(f"Error training {name}: {e}")
                    pass
                    
        return results
