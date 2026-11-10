MODELS_INSERT = """
   INSERT INTO models (name) VALUES ('Наивный прогноз') ON CONFLICT DO NOTHING;
   INSERT INTO models (name) VALUES ('Линейная модель') ON CONFLICT DO NOTHING;
   INSERT INTO models (name) VALUES ('Градиентный бустинг') ON CONFLICT DO NOTHING;
"""