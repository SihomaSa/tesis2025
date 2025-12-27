def train_model(self):
    """Entrena un nuevo modelo de clasificación"""
    try:
        print("🔍 Debug: Iniciando train_model()")
        
        # ... tu código existente hasta la creación del modelo
        
        print(f"🔍 Debug: Creando VotingClassifier...")
        ensemble_model = VotingClassifier(estimators=[
            ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
            ('xgb', XGBClassifier(n_estimators=100, use_label_encoder=False, eval_metric='logloss', random_state=42)),
            ('svm', SVC(probability=True, random_state=42))
        ])
        
        print(f"🔍 Debug: ensemble_model creado: {ensemble_model}")
        print(f"🔍 Debug: Tipo: {type(ensemble_model)}")
        
        self.model = ensemble_model
        print(f"🔍 Debug: self.model asignado: {self.model}")
        print(f"🔍 Debug: self.model es None? {self.model is None}")
        
        # Línea 617 - agregar más debug
        print(f"🔍 Debug: Antes de fit(), X_train_bal shape: {X_train_bal.shape}")
        print(f"🔍 Debug: Antes de fit(), y_train_bal shape: {y_train_bal.shape}")
        
        self.model.fit(X_train_bal, y_train_bal)  # Línea 617
        print("🔍 Debug: fit() completado exitosamente")
        
    except Exception as e:
        print(f"🔍 Debug: ERROR en train_model: {e}")
        print(f"🔍 Debug: Tipo de error: {type(e)}")
        raise