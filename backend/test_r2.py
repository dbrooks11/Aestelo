from app import create_app, db
app = create_app()

def bucket_test():

    with app.app_context():
        # Test 1: Connection
        try:
            db.engine.connect()
            db.drop_all()
            print("✅ Database connected!")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            exit()
        
    
if __name__ == "__main__":
    bucket_test()