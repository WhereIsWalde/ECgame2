from dotenv import load_dotenv
import oracledb
import os

if __name__ == "__main__":
    
    load_dotenv()
    DB_USER = "ADMIN"
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_CONNECT_STRING = '(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.eu-stockholm-1.oraclecloud.com))(connect_data=(service_name=ge72a74000425b4_ecgame_tp.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'
    #os.environ.get("DB_CONNECT_STRING")

    try:
        # Try a direct connection first to rule out pool issues
        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_CONNECT_STRING
        )
        print("Connection successful!")

        with conn.cursor() as cursor:
            query: str = """
                CREATE TABLE players (
                            user_id INTEGER,
                            game_id INTEGER,
                            state_name TEXT,
                            leader_name TEXT
                        );
                        """
            cursor.execute(query)
            
        conn.close()

    except oracledb.Error as e:
        print(f"Error: {e}")



