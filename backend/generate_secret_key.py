#!/usr/bin/env python3
"""
Script para generar una SECRET_KEY segura para JWT
"""
import secrets

if __name__ == "__main__":
    secret_key = secrets.token_urlsafe(32)
    print("\n" + "="*60)
    print("SECRET_KEY generada para JWT")
    print("="*60)
    print(f"\n{secret_key}\n")
    print("Copia esta clave y añádela a tu archivo .env:")
    print(f"\nSECRET_KEY={secret_key}\n")
    print("="*60)
