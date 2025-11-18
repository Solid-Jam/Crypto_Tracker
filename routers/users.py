import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.user import User, UserCreate
from database import get_db_connection
from auth.security import get_api_key

router = APIRouter()

@router.get('/', response_model=List[User])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM users')
    users = cursor.fetchall()
    conn.close()
    return [{
        "id": user[0],
        "name": user[1]
    } for user in users]

@router.post('/', response_model=User)
def create_user(
        user: UserCreate,
        _: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (name) VALUES (?)", (user.name,))
        conn.commit()
        user_id = cursor.lastrowid
        return User(id=user_id, name=user.name)
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The user '{user.name}' already exists."
        )
    finally:
        conn.close()

@router.put('/{user_id}', response_model=User)
def update_user(
        user_id: int,
        user: UserCreate,
        _: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET name = ? WHERE id = ?", (user.name, user))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail='User not found')
    conn.commit()
    conn.close()
    return User(id=user_id, name=user.name)


@router.delete('/{user_id}', response_model=dict)
def delete_user(
        user_id: int,
        _: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail='User not found')
    conn.commit()
    conn.close()
    return {
        "detail": "User deleted"
    }