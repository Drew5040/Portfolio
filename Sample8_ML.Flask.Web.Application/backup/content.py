from sqlalchemy import Column, Integer, String, Text, JSON, ARRAY, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Metadata(Base):
    __tablename__ = 'metadata'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    content = Column(Text)
    page = Column(String(255))


class NavigationLink(Base):
    __tablename__ = 'navigation_links'
    id = Column(Integer, primary_key=True)
    label = Column(String(255))
    urls = Column(String(255))
    title = Column(String(255))
    target = Column(String(50))
    rel = Column(String(100), nullable=True)


class Footer(Base):
    __tablename__ = 'footer'
    id = Column(Integer, primary_key=True)
    text_content = Column(Text)
    privacy_policy_url = Column(String(255))


class WelcomePage(Base):
    __tablename__ = 'welcome_page'
    id = Column(Integer, primary_key=True)
    profile_image_url = Column(Text)
    name = Column(String(255))
    qualification = Column(Text)
    institution_logo_url = Column(Text)
    institution_name = Column(String(255))
    intro_header = Column(Text)
    intro_text = Column(Text)
    usp_data = Column(JSON)


class AboutPage(Base):
    __tablename__ = 'about_page'
    id = Column(Integer, primary_key=True)
    page_title = Column(String(255))
    project_overview = Column(Text)
    contact_email = Column(String(255))
    additional_info = Column(Text, nullable=True)


class ModelPage(Base):
    __tablename__ = 'model_page'
    id = Column(Integer, primary_key=True)
    page_header = Column(String(255))
    logos_urls = Column(ARRAY(Text))


class ContactSubmissions(Base):
    __tablename__ = 'contact_submissions'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    submission_date = Column(TIMESTAMP)
