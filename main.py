from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
import requests
import os
from contextlib import asynccontextmanager
