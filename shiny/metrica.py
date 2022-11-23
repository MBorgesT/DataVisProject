import pandas as pd
import sqlalchemy as db
import plotly.express as px


class MetricasPlot:


    def __init__(self):
        connection_str = f'mysql+pymysql://root:admin@172.17.0.2:3306/imdb'
        engine = db.create_engine(connection_str)
        self.conn = engine.connect()
        
        self._init_dfs()
        
        
    def _init_dfs(self):
        query = '''
            SELECT tr.averageRating, tr.numVotes, ta.title
            FROM title_basics AS tb
            LEFT JOIN title_ratings AS tr ON tb.tconst = tr.tconst
            LEFT JOIN title_akas AS ta ON tb.tconst = ta.titleId
        '''
        self.df1 = pd.read_sql(query, self.conn)
        
        
    def get_scatter_1(self, vline):
        fig = px.scatter(
            self.df1, y='averageRating', x='numVotes', 
            custom_data=['averageRating', 'numVotes', 'title'],
            log_x=True
        )
        fig.update_traces(
            hovertemplate="<br>".join([
                "AvgRating: %{customdata[0]}",
                "NumVotes: %{customdata[1]}",
                "Title: %{customdata[2]}",
            ])
        )
        if vline > 0:
            fig.add_vline(vline)
        return fig