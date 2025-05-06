import re
from PyPDF2 import PdfReader
from docx import Document


class ResumeReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.text = self._load_text()

    def _load_text(self):
        ext = self.filepath[self.filepath.rfind('.'):].lower()
        if ext == '.pdf':
            return self._extract_text_pdf()
        elif ext == '.docx':
            return self._extract_text_docx()
        else:
            raise ValueError(f"Unsupported file type: {ext}. Only .pdf and .docx are supported.")

    def _extract_text_pdf(self):
        text = ''
        try:
            with open(self.filepath, 'rb') as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text() or ''
                    text += page_text + '\n'
        except FileNotFoundError:
            raise FileNotFoundError(f"PDF file not found: {self.filepath}")
        except Exception as e:
            raise IOError(f"Error reading PDF file: {e}")
        return text.lower()

    def _extract_text_docx(self):
        text = ''
        try:
            doc = Document(self.filepath)
            for para in doc.paragraphs:
                text += para.text + '\n'
        except FileNotFoundError:
            raise FileNotFoundError(f"DOCX file not found: {self.filepath}")
        except Exception as e:
            raise IOError(f"Error reading DOCX file: {e}")
        return text.lower()

    def extract_email(self):
        match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", self.text)
        return match.group(0) if match else None

    def extract_name(self):
        # Assume the first non-empty line is the candidate's name
        lines = [line.strip() for line in self.text.splitlines() if line.strip()]
        return lines[0].title() if lines else None

    def extract_skills(self, all_skills):
        found = []
        for skill in all_skills:
            pattern = rf"\b{re.escape(skill.lower())}\b"
            if re.search(pattern, self.text):
                found.append(skill)
        return found
