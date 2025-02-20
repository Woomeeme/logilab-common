# copyright 2003-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-common.
#
# logilab-common is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License,
# or (at your option) any later version.
#
# logilab-common is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with logilab-common.  If not, see <http://www.gnu.org/licenses/>.
"""HTML formatting drivers for ureports"""
__docformat__ = "restructuredtext en"

from logilab.common.ureports.html_writer import HTMLWriter


class DocbookWriter(HTMLWriter):
    """format layouts as HTML"""

    def begin_format(self, layout):
        """begin to format a layout"""
        super(HTMLWriter, self).begin_format(layout)
        if self.snippet is None:
            self.writeln('<?xml version="1.0" encoding="ISO-8859-1"?>')
            self.writeln(
                """
<book xmlns:xi='http://www.w3.org/2001/XInclude'
      lang='fr'>
"""
            )

    def end_format(self, layout):
        """finished to format a layout"""
        if self.snippet is None:
            self.writeln("</book>")

    def visit_section(self, layout):
        """display a section (using <chapter> (level 0) or <section>)"""
        if self.section == 0:
            tag = "chapter"
        else:
            tag = "section"
        self.section += 1
        self.writeln(self._indent(f"<{tag}{self.handle_attrs(layout)}>"))
        self.format_children(layout)
        self.writeln(self._indent(f"</{tag}>"))
        self.section -= 1

    def visit_title(self, layout):
        """display a title using <title>"""
        self.write(self._indent(f"  <title{self.handle_attrs(layout)}>"))
        self.format_children(layout)
        self.writeln("</title>")

    def visit_table(self, layout):
        """display a table as html"""
        self.writeln(
            self._indent(f"  <table{self.handle_attrs(layout)}><title>{layout.title}</title>")
        )
        self.writeln(self._indent(f'    <tgroup cols="{layout.cols}">'))
        for i in range(layout.cols):
            self.writeln(self._indent(f'      <colspec colname="c{i}" colwidth="1*"/>'))

        table_content = self.get_table_content(layout)
        # write headers
        if layout.cheaders:
            self.writeln(self._indent("      <thead>"))
            self._write_row(table_content[0])
            self.writeln(self._indent("      </thead>"))
            table_content = table_content[1:]
        elif layout.rcheaders:
            self.writeln(self._indent("      <thead>"))
            self._write_row(table_content[-1])
            self.writeln(self._indent("      </thead>"))
            table_content = table_content[:-1]
        # write body
        self.writeln(self._indent("      <tbody>"))
        for i in range(len(table_content)):
            row = table_content[i]
            self.writeln(self._indent("        <row>"))
            for j in range(len(row)):
                cell = row[j] or "&#160;"
                self.writeln(self._indent(f"          <entry>{cell}</entry>"))
            self.writeln(self._indent("        </row>"))
        self.writeln(self._indent("      </tbody>"))
        self.writeln(self._indent("    </tgroup>"))
        self.writeln(self._indent("  </table>"))

    def _write_row(self, row):
        """write content of row (using <row> <entry>)"""
        self.writeln("        <row>")
        for j in range(len(row)):
            cell = row[j] or "&#160;"
            self.writeln(f"          <entry>{cell}</entry>")
        self.writeln(self._indent("        </row>"))

    def visit_list(self, layout):
        """display a list (using <itemizedlist>)"""
        self.writeln(self._indent(f"  <itemizedlist{self.handle_attrs(layout)}>"))
        for row in list(self.compute_content(layout)):
            self.writeln(f"    <listitem><para>{row}</para></listitem>")
        self.writeln(self._indent("  </itemizedlist>"))

    def visit_paragraph(self, layout):
        """display links (using <para>)"""
        self.write(self._indent("  <para>"))
        self.format_children(layout)
        self.writeln("</para>")

    def visit_span(self, layout):
        """display links (using <p>)"""
        # TODO: translate in docbook
        self.write(f"<literal {self.handle_attrs(layout)}>")
        self.format_children(layout)
        self.write("</literal>")

    def visit_link(self, layout):
        """display links (using <ulink>)"""
        self.write(
            '<ulink url="{}"{}>{}</ulink>'.format(
                layout.url, self.handle_attrs(layout), layout.label
            )
        )

    def visit_verbatimtext(self, layout):
        """display verbatim text (using <programlisting>)"""
        self.writeln(self._indent("  <programlisting>"))
        self.write(layout.data.replace("&", "&amp;").replace("<", "&lt;"))
        self.writeln(self._indent("  </programlisting>"))

    def visit_text(self, layout):
        """add some text"""
        self.write(layout.data.replace("&", "&amp;").replace("<", "&lt;"))

    def _indent(self, string):
        """correctly indent string according to section"""
        return " " * 2 * (self.section) + string
