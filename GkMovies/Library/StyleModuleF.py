from app import db
from app.models import User, AdderColumn, UserColumn
from flask_login import current_user
from sqlalchemy.sql import func
    
class Style:
    
    def getCommonStyle(self):
        style = """
        
    .button_up {
        border: 1px solid #555555;
        border-radius: 5px;
        background-color: #D6EAF8;
        color:blue;
        font-family: Helvetica;
        font-size: 13px;
        cursor: pointer;
        padding-top: 5px;
        padding-bottom: 5px;
        box-shadow: -2px -2px 6px 2px rgba(0,0,0,0.5) inset;
    }
    
    .button_down {
        border: 1px solid #555555;
        border-radius: 5px;
        background-color: #D6EAF8;
        color:red;
        font-weight: bold;
        font-family: Helvetica;
        font-size: 13px;
        cursor: pointer;
        padding-top: 5px;
        padding-bottom: 5px;
        box-shadow: 2px 2px 6px 2px rgba(0,0,0,0.5) inset;
    }
    
    .button_small {
        border: 1px solid #555555;
        border-radius: 5px;
        background-color: #D6EAF8;
        color:blue;
        font-family: Helvetica;
        font-size: 13px;
        cursor: pointer;
        padding-top: 1px;
        padding-bottom: 3px;
        box-shadow: -2px -2px 5px 2px rgba(0,0,0,0.4) inset;
    }
    
    .eye_inside i {
        margin-left: -20px;
        cursor: pointer;
    }

    .eye_outside i {
        margin-left: 5px;
        cursor: pointer;
    }
    
            
    .title_bold {
        font-family: Helvetica;
        font-size: 14px;
        font-weight: bold;
    }
    
    .title_bold_special {
        font-family: Helvetica;
        font-size: 15px;
        font-weight: bold;
        color: green;
    }
    
    .hide_slide {
        display: inline-block;
        vertical-align: top;
        overflow: hidden;
        border: solid grey 0px;
        outline:none;
    }

    .hide_slide select {
        padding: 10px;
        margin: -5px -20px -5px -5px;
    }
    
    
    h2 {
        font-family: Helvetica;
        font-size: 20px;
        margin-bottom: -1px;
    }
    
    h4 {
        font-family: Helvetica;
        font-size: 16px;
        margin-bottom: 10px;
    }
    
    hr.club {
        margin-top: 24px;
        margin-bottom: -10px;
        max-width: 400px;
        text-align: left;
        margin-left: 0;
    }
    
    a.helv {
        font-family: Helvetica;
        font-size: 14px;
        text-decoration: none;
        color:blue;
    }
    
    a.helv_large {
        font-family: Helvetica;
        font-size: 15px;
        text-decoration: none;
        color:blue;
    }
    
    a.imdb:link {
        font-family: Helvetica;
        font-size: 13px;
        text-decoration: none;
        color:blue;
    }
    
    a.imdb:visited {
        font-family: Helvetica;
        font-size: 13px;
        text-decoration: none;
        color:purple;
    }

    a.imdb_large:link {
        font-family: Helvetica;
        font-size: 15px;
        text-decoration: none;
        color:blue;
    }
    
    a.imdb_large:visited {
        font-family: Helvetica;
        font-size: 15px;
        text-decoration: none;
        color:purple;
    }
    
    a.helv_small {
        font-family: Helvetica;
        font-size: 13px;
        text-decoration: none;
        color:blue;
    }
    
    a.helv_smaller {
        font-family: Helvetica;
        font-size: 12px;
        text-decoration: none;
        color:blue;
    }
        
    a.poster_link_font {
        font-family: Helvetica;
        font-size: 16px;
        font-weight: bold;
        text-align: left;
        text-decoration: none;
    }
    
    a.h4 {
        font-family: Helvetica;
        font-size: 16px;
        text-decoration: none;
        color:blue;
    }
    
    div.helv {
        font-family: Helvetica;
        font-size: 14px;
    }
    
    div.helv_small {
        font-family: Helvetica;
        font-size: 13px;
    }
    
    div.helv_small_color {
        font-family: Helvetica;
        font-size: 13px;
        color: red;
    }
    
    div.helv_large {
        font-family: Helvetica;
        font-size: 15px;
    }
    
    
    div.helv_section {
        font-family: Helvetica;
        font-size: 14px;
        width: 750px;
    }

    div.base_spinner {
        display:none;
        position: absolute; 
        top: 40px;
        left: 560px;
    }
    
    
    div.tight {
        margin-top: -9px;
        margin-bottom: -9px;
    }
    
    div.button_sort {
        font-family: Helvetica;
        font-size: 14px;
        display: inline-block;
        padding-top: 9px;
        padding-bottom: 8px;
    }
               
    div.scrollable {
        width: 100%;
        padding: 0;
        overflow: auto;
    }
     
    div.scrollable_auto {
        width: 100%;
        padding-left: 5;
        padding-right: 5;
        overflow: auto;
        font-family: Helvetica; 
        font-size: 13px;
    }

    li.helv {
        font-family: Helvetica;
        font-size: 13px;
    }

    span.helv_small {
        font-family: Helvetica;
        font-size: 13px;
    }
    
    span.helv {
        font-family: Helvetica;
        font-size: 14px;
    }
    
    span.helv_large {
        font-family: Helvetica;
        font-size: 16px;
    }
    

    
    span.light_bold {
        font-family: Helvetica;
        font-weight: normal;
        color: blue;
        font-size: 14px;
    }

    td.helv_small {
        font-family: Helvetica;
        font-size: 13px;
    }
    
    td.helv  {
        font-family: Helvetica;
        font-size: 14px;
    }
    
    th.helv_bold  {
        font-family: Helvetica;
        font-size: 14px;
        font-weight: bold;
    }
    
    td.poster_font {
        font-family: Helvetica;
        font-size: 16px;
        font-weight: bold;
        text-align: left;
    }
    
    td.movie_review_title {
        vertical-align: top;
        padding-top: 0px;
        font-family: Helvetica;
        font-size: 18px;
    }

    td.noborder {
        border-bottom: 0px;
        border-left: 0px;
        border-right: 0px;
    }
    
    td.noborder_left {
        text-align: left;
        border-bottom: 0px;
        border-left: 0px;
        border-right: 0px;
    }
    
    td.noborder_center {
        width: 80px;
        text-align: center;
        border-bottom: 0px;
        border-left: 0px;
        border-right: 0px;
    }
    
    
    ul.version  {
        padding-left: 14px;
    }
    
    li.version {
        padding-bottom: 8px;
    }
    
    """
        return style

    def getHomeStyle(self):
        style = self.getCommonStyle() + """

    table.home, td.home, th.home  {
        font-family: Helvetica;
        font-size: 14px;
        padding-top: 5px;
        padding-left: 5px;
        padding-right: 2px;
        padding-bottom: 15px;
        border-collapse: collapse;
        border-spacing: 0px;
        border: 1px solid black;
    }

    """
    
        return style
    
    def getAdderStyle(self):
            
        style = self.getCommonStyle() + """
        
    table.border {
        border: 1px solid #222222;
        border-collapse: collapse; 
    }
    
    tr.alt:nth-child(even) {
      background-color: #e0e0e0;
    }

    td.border_top {
        vertical-align: top;
        border: 1px solid #222222;
        padding-left: 3px;
        padding-right: 3px;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 13px;
    }
    
    td.border_top_scroll {
        vertical-align: top;
        text-align: center;        
        border: 1px solid #222222;
        padding-left: 3px;
        padding-right: 0px;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 13px;
    }
    
    td.border_middle {
        vertical-align: middle;
        text-align: center;
        border: 1px solid #222222;
        padding-left: 3px;
        padding-right: 3px;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 13px;
    }
    
    td.border_none {
        border: 0px;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 13px;
    }
    
    div.genres_selected {
        padding-left: 365px;
        font-family: Helvetica;
        font-size: 17px;
        font-weight: bold;
        color: LimeGreen;
    }
    
    div.no_movies {
        padding-left: 300px;
        font-family: Helvetica;
        font-size: 16px;
    }
    
    """
            
        return style
   
       
    def getDisplayStyle(self, user, cuser, displayType, bodyHeight):
        #user = User.query.filter(User.login == current_user.login).join(UserColumn).first()

        tableWidth = user.getTableWidth(cuser, displayType)
        cols = user.getNumCols()
        tableWidth += cols * 4 + 14

        
        style = self.getCommonStyle() + """

    
    table.title_table {
        height: 40px;
        width: """ + str(tableWidth) + """px;
        color: #222222;
        vertical-align: middle;
        text-align: left;
        border-collapse: collapse;  
        border-top: 1px solid #222222;
        border-right: 1px solid #222222;
    }

    
    
    td.found_cell {
        width: 500px;
        text-indent: 30px;
        border-right: 0px;
    }
    
    td.page_cell {
        text-align: left;
        border-left: 0px;
        border-right: 0px;

    }
    
    td.page_number_cell {
        width: 25px;
        text-align: center;
        border-top: 1px solid #00008B;
        border-bottom: 1px solid #00008B;
        border-left: 1px solid #00008B;
        border-right: 1px solid #00008B;
    }
    
    td.per_page_cell {
        width: 100x;
        border-top: 0px;
        border-bottom: 0px;
        border-left: 0px;
        border-right: 0px;
    }
    
    td.arrow_page_cell {
        border-top: 0px;
        border-bottom: 0px;
        border-left: 0px;
        border-right: 0px;
    }
    


    
    td.actor {
        border: 1px solid;
        text-align: right;
    }
    
    a.page_text:visited {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 17px;
        text-decoration: none;
        color:blue;
    }
    
    a.page_text:link {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 17px;
        text-decoration: none;
        color:blue;

    }
    
    .title_text {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 24px;
    }
    .found_text {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 18px;
    }
    
    
    .fixed_headers {
        width: """ + str(tableWidth) + """px;
        table-layout: fixed; 
        border-collapse: collapse;  
    }
    .fixed_headers table, th, td {
        border-top: 0px solid #222222;
        border-left: 1px solid #222222;
        border-right: 1px solid #222222;
        border-bottom: 1px solid #222222;
    }
    
    .fixed_headers thead td {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 15px;
        text-align: center;
        vertical-align: top;
    }
    .fixed_headers tbody td {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 13px;
        vertical-align: top;
    }\n
    .fixed_headers thead td text {
        padding-bottom: 2px;
    }\n"""
    
       
        c = 1
        for col in user.getColumns(cuser, displayType):
            if col.vis == 'T':
                style += '    .fixed_headers thead td:nth-child(' + str(c) + ') {\n'
                style += '        width: ' + str(col.getWidth()) + 'px;\n'
                style += '    }\n'
                style += '    .fixed_headers tbody td:nth-child(' + str(c) + ') {\n'
                style += '        width: ' + str(col.getWidth()) + 'px;\n'
                style += '        text-align: ' + col.attribute.align + ';\n'
                style += '        vertical-align: ' + col.attribute.valign + ';\n'
                style += '    }\n'
                c += 1
                    
                
        style += """
    .fixed_headers thead {
      background-color: #EBF5FB;
      color: #222222;
    }
    .fixed_headers thead tr {
      display: table;
      position: relative;
    }
    .fixed_headers tbody {
      display: block;
      overflow: auto;
      height: """ + bodyHeight + """px;
    }
    .fixed_headers tbody tr:nth-child(even) {
      background-color: #e0e0e0;
    }
    
        
    .filter {
        font-family: Helvetica;
        font-size: 17px;
        font-weight: bold;
        color: LimeGreen;
    }
    
    ::placeholder {
        font-family: Helvetica;
        font-size: 12px;
        font-weight: normal;
        color: grey;
    }

    .old_ie_wrapper {
      height: """ + bodyHeight + """px;
      width: """ + str(tableWidth)  + """px;
      overflow-x: hidden;
      overflow-y: auto;
    }
    .old_ie_wrapper tbody {
      height: auto;
    }\n"""
            
        return style

    def getHelpStyle(self):
        style = """
        
    div.helv_section {
        font-family: Helvetica;
        font-size: 14px;
        width: 600px;
    }
    
    div.helv {
        font-family: Helvetica;
        font-size: 14px;
    }
    
    a.helv {
        font-family: Helvetica;
        font-size: 14px;
        text-decoration: none;
        color:blue;
    }
    
    span.light_bold {
        font-family: Helvetica;
        font-weight: normal;
        color: blue;
        font-size: 14px;
    }
    
    .button_small {
        border: 1px solid #555555;
        border-radius: 5px;
        background-color: #D6EAF8;
        color:blue;
        font-family: Helvetica;
        font-size: 13px;
        cursor: pointer;
        padding-top: 1px;
        padding-bottom: 3px;
        box-shadow: -2px -2px 5px 2px rgba(0,0,0,0.4) inset;
    }

    """
    
        return style
    
