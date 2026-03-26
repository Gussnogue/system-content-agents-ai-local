import os
from docx import Document
from docx.shared import Cm, Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import re

class AbntFormatter:
    """
    Aplica formatação ABNT em um documento .docx.
    """

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.doc = Document(input_path)

    def apply_abnt(self):
        """Executa todas as etapas de formatação."""
        self._set_margins()
        self._set_default_font()
        self._apply_paragraph_spacing()
        self._apply_headings()
        self._apply_tables()
        self._apply_page_numbers()
        self._save()

    def _set_margins(self):
        """Define margens: superior 3cm, inferior 2cm, esquerda 3cm, direita 2cm."""
        section = self.doc.sections[0]
        section.top_margin = Cm(3)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(3)
        section.right_margin = Cm(2)

    def _set_default_font(self):
        """Define fonte padrão como Arial 12, espaçamento 1.5, sem espaçamento extra."""
        style = self.doc.styles['Normal']
        font = style.font
        font.name = 'Arial'
        font.size = Pt(12)
        paragraph_format = style.paragraph_format
        paragraph_format.line_spacing = 1.5
        paragraph_format.space_before = Pt(0)
        paragraph_format.space_after = Pt(0)
        paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def _apply_paragraph_spacing(self):
        """Garante que todos os parágrafos (exceto títulos) tenham recuo de primeira linha."""
        for para in self.doc.paragraphs:
            # Se não for título (baseado em estilo), aplica recuo
            if not para.style.name.startswith('Heading'):
                para.paragraph_format.first_line_indent = Cm(1.25)  # recuo de 1,25cm
                para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def _apply_headings(self):
        """
        Detecta títulos baseado em padrões (numeração) e aplica estilos.
        Título 1: números romanos ou arábicos em maiúsculas, exemplo: "1 INTRODUÇÃO"
        Título 2: "1.1 OBJETIVOS"
        Título 3: "1.1.1 ..."
        """
        heading_patterns = [
            (r'^\d+\.?\d*\.?\d*\s+[A-ZÇÃÕÁÉÍÓÚÂÊÎÔÛÀ][A-ZÇÃÕÁÉÍÓÚÂÊÎÔÛÀ\s]+$', 1),  # Título 1
            (r'^\d+\.\d+\s+[A-ZÇÃÕÁÉÍÓÚÂÊÎÔÛÀ][A-ZÇÃÕÁÍÓÚÂÊÎÔÛÀ\s]+$', 2),       # Título 2
            (r'^\d+\.\d+\.\d+\s+[A-ZÇÃÕÁÉÍÓÚÂÊÎÔÛÀ][A-ZÇÃÕÁÍÓÚÂÊÎÔÛÀ\s]+$', 3),   # Título 3
        ]

        # Garantir que os estilos Heading existam
        self._ensure_heading_styles()

        for para in self.doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue

            for pattern, level in heading_patterns:
                if re.match(pattern, text):
                    style_name = f'Heading {level}'
                    para.style = self.doc.styles[style_name]
                    # Formatação específica ABNT
                    para.paragraph_format.space_before = Pt(12)
                    para.paragraph_format.space_after = Pt(12)
                    para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    break
            else:
                # Se não for título, mantém como Normal
                pass

    def _ensure_heading_styles(self):
        """Cria estilos de heading se não existirem, e configura conforme ABNT."""
        for i in range(1, 4):
            style_name = f'Heading {i}'
            if style_name not in self.doc.styles:
                style = self.doc.styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
            else:
                style = self.doc.styles[style_name]
            font = style.font
            font.name = 'Arial'
            font.size = Pt(12)
            font.bold = True
            # Para Heading 1, letras maiúsculas
            if i == 1:
                font.all_caps = True
            style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            style.paragraph_format.space_before = Pt(12)
            style.paragraph_format.space_after = Pt(12)

    def _apply_tables(self):
        """Aplica formatação básica às tabelas (bordas, fonte)."""
        for table in self.doc.tables:
            # Define fonte para células
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        for run in para.runs:
                            run.font.name = 'Arial'
                            run.font.size = Pt(10)
                            run.font.bold = False
            # Adiciona bordas (simples)
            tbl = table._element
            tblPr = tbl.tblPr
            if tblPr is None:
                tblPr = OxmlElement('w:tblPr')
                tbl.insert(0, tblPr)
            # Adiciona borda padrão
            borders = OxmlElement('w:tblBorders')
            for edge in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
                edge_elem = OxmlElement(f'w:{edge}')
                edge_elem.set(qn('w:val'), 'single')
                edge_elem.set(qn('w:sz'), '4')
                edge_elem.set(qn('w:space'), '0')
                edge_elem.set(qn('w:color'), 'auto')
                borders.append(edge_elem)
            tblPr.append(borders)

    def _apply_page_numbers(self):
        """Adiciona número de página no canto superior direito (folha de rosto não)."""
        section = self.doc.sections[0]
        header = section.header
        # Cria um parágrafo no cabeçalho
        p = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run = p.add_run()
        # Insere número de página
        fld_char = OxmlElement('w:fldChar')
        fld_char.set(qn('w:fldCharType'), 'begin')
        run._r.append(fld_char)
        instr_text = OxmlElement('w:instrText')
        instr_text.text = 'PAGE'
        run._r.append(instr_text)
        fld_char_end = OxmlElement('w:fldChar')
        fld_char_end.set(qn('w:fldCharType'), 'end')
        run._r.append(fld_char_end)

    def _save(self):
        self.doc.save(self.output_path)

        