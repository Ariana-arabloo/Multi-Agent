from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship
from pgvector.sqlalchemy import Vector
import datetime

Base = declarative_base()

# مدل‌های قبلی (Projects و AgentNode)
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    nodes = relationship("AgentNode", back_populates="project", cascade="all, delete-orphan")


class AgentNode(Base):
    __tablename__ = "agent_nodes"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    node_type = Column(String(100), nullable=True)
    embedding = Column(Vector(1536), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="nodes")


# مدل جدید: execution_states با فیلد JSONB
class ExecutionState(Base):
    __tablename__ = "execution_states"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # فیلد state از نوع JSONB برای ذخیره‌سازی داده‌های ساختاریافته و منعطف
    state_data = Column(JSONB, nullable=False, default={})
    
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    project = relationship("Project")


# مدل جدید: message_log همراه با Index ترکیبی
class MessageLog(Base):
    __tablename__ = "message_log"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    sender = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    logged_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project")

    # تعریف ایندکس ترکیبی روی دو ستون project_id و logged_at برای بهبود سرعت جستجو
    __table_args__ = (
        Index('idx_project_logged_at', 'project_id', 'logged_at'),
    )
    # مدل مالی: token_ledgers برای مدیریت توکن‌ها
class TokenLedger(Base):
    __tablename__ = "token_ledgers"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    tokens_used = Column(Integer, nullable=False, default=0)
    cost = Column(Integer, nullable=False, default=0)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project")


# مدل حقوقی/انسانی: human_interventions برای نظارت‌های انسانی
class HumanIntervention(Base):
    __tablename__ = "human_interventions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project")