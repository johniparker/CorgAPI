import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from CorgAPI.database.rds_conn import create_conn

class RacetimePredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.preprocessor = ColumnTransformer(
        transformers=[
            ('breed', OneHotEncoder(drop='first'), ['breed']),
            ('gender', OneHotEncoder(drop='first'), ['gender'])
            ],
            remainder='passthrough'
        )
        self.trained_model = self.load_and_train()
        
    def load_and_train(self):
        conn = create_conn()
        query = """
        select 
            c.corgid,
            c.age, 
            c.weight, 
            c.breed, 
            c.gender, 
            o.racetime
        from
            corgi c 
            join outcome o on c.corgid = o.corgid
        ;
        """
        df = pd.read_sql(query, conn, index_col="corgid")
        conn.close()
            
        X = df[['age', 'weight', 'breed', 'gender']]
        y = df['racetime']
        
        X_encoded = self.preprocessor.fit_transform(X)
        self.model.fit(X_encoded, y)
                
        test_score = self.model.score(X_encoded, y)
        print(f"model r2 score on full dataset: {test_score}")
        
        return self.model
        
    def predict_racetime(self, user_features):
        features = user_features[['age', 'weight', 'breed', 'gender']]
        #map categorical features to numerical values
        user_features_encoded = self.preprocessor.transform(features)
        predicted_racetime = self.trained_model.predict(user_features_encoded)[0]
        return round(predicted_racetime, 2)
       