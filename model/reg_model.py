import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from CorgAPI.database.rds_conn import create_conn

def load_and_train():
    model = LinearRegression()
    
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
            
    model.fit(X, y)
            
    test_score = self.model.score(X, y)
    print(f"model r2 score on full dataset: {test_score}")
    
    return model

trained_model = load_and_train()
    
def predict_racetime(self, user_features):
    estimated_racetime = self.model.predict([user_features])[0]
    return round(estimated_racetime, 2)
   