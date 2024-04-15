"""
This module defines the SQLAlchemy ORM models for a web application's database
schema. Each class corresponds to a table in the database and is used to interact
with the corresponding data.

Classes:
    Metadata: Represents metadata information for various pages or sections of the website.
    NavigationLink: Represents navigation links in the website's menu.
    Footer: Represents the content of the website's footer section.
    WelcomePage: Represents content specific to the welcome or home page of the website.
    AboutPage: Represents content specific to the about page of the website.
    ModelPage: Represents content specific to a model showcase page of the website.
    ContactSubmissions: Represents entries submitted through the website's contact form.
"""

from sqlalchemy import Column, Integer, String, Text, JSON, ARRAY, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Metadata(Base):
    """
    Represents metadata information like page titles, descriptions, etc., for various pages
    or sections of the website.

    Attributes:
        id (Integer): The primary key.
        name (String): The name of the metadata element.
        content (Text): The content of the metadata element.
        page (String): Reference to the page or section this metadata belongs to.
    """
    __tablename__ = 'metadata'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    content = Column(Text)
    page = Column(String(255))


class NavigationLink(Base):
    """
    Represents a navigation link in the website's menu, including label, URL, and other attributes.

    Attributes:
        id (Integer): The primary key.
        label (String): The text label of the navigation link.
        urls (String): The URL the navigation link points to.
        title (String): The title attribute of the link.
        target (String): The target attribute of the link (e.g., _blank, _self).
        rel (String): The rel attribute of the link (optional).
    """
    __tablename__ = 'navigation_links'
    id = Column(Integer, primary_key=True)
    label = Column(String(255))
    urls = Column(String(255))
    title = Column(String(255))
    target = Column(String(50))
    rel = Column(String(100), nullable=True)


class Footer(Base):
    """
    Represents the content of the website's footer section, including text content and
    privacy policy URL.

    Attributes:
        id (Integer): The primary key.
        text_content (Text): The text content displayed in the footer.
        privacy_policy_url (String): The URL to the privacy policy page.
    """
    __tablename__ = 'footer'
    id = Column(Integer, primary_key=True)
    text_content = Column(Text)
    privacy_policy_url = Column(String(255))


class WelcomePage(Base):
    """
    Represents content specific to the welcome or home page, including personal
    information and introductory text.

    Attributes:
        id (Integer): The primary key.
        profile_image_url (Text): URL of the profile image.
        name (String): Name of the individual or entity featured on the page.
        qualification (Text): Qualification or title of the individual or entity.
        institution_logo_url (Text): URL of the institution or company logo.
        institution_name (String): Name of the institution or company.
        intro_header (Text): Header text for the introduction section.
        intro_text (Text): Body text for the introduction section.
        usp_data (JSON): JSON data containing unique selling points or key features.
    """
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
    """
    Represents content specific to the about page, including project overview and
    contact information.

    Attributes:
        id (Integer): The primary key.
        page_title (String): The title of the about page.
        project_overview (Text): Overview or description of the project.
        contact_email (String): Contact email address for the project or entity.
        additional_info (Text): Additional information about the project or entity (optional).
    """
    __tablename__ = 'about_page'
    id = Column(Integer, primary_key=True)
    page_title = Column(String(255))
    project_overview = Column(Text)
    contact_email = Column(String(255))
    additional_info = Column(Text, nullable=True)


class ModelPage(Base):
    """
    Represents content specific to a model showcase page, including header and logos.

    Attributes:
        id (Integer): The primary key.
        page_header (String): The header or title of the model page.
        logos_urls (ARRAY(Text)): List of URLs for logos displayed on the page.
    """
    __tablename__ = 'model_page'
    id = Column(Integer, primary_key=True)
    page_header = Column(String(255))
    logos_urls = Column(ARRAY(Text))


class ContactSubmissions(Base):
    """
    Represents entries submitted through the website's contact form, storing user contact
    information and messages.

    Attributes:
        id (Integer): The primary key.
        email (String): The email address of the individual submitting the form.
        name (String): The name of the individual submitting the form.
        subject (String): The subject of the message submitted.
        message (Text): The text of the message submitted.
        submission_date (TIMESTAMP): The date and time the submission was made.
    """
    __tablename__ = 'contact_submissions'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    submission_date = Column(TIMESTAMP)
