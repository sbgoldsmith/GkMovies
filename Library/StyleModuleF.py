from app import db
from app.models import User, AdderColumn, UserColumn
from flask_login import current_user
from sqlalchemy.sql import func
    
class Style:
    
    def getCommonStyle(self):
        style = """
    h2 {
        font-family: Helvetica;
        font-size: 20px;
    }
    
    li.helv {
        font-family: Helvetica;
        font-size: 13px;
    }

    a.helv {
        font-family: Helvetica;
        font-size: 14px;
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
    
    
    div.helv_section {
        font-family: Helvetica;
        font-size: 14px;
        width: 650px;
    }

    td.helv  {
        font-family: Helvetica;
        font-size: 14px;
    }
    
    
    td.noborder {
        border-bottom: 0px;
        border-left: 0px;
        border-right: 0px;
    }
    
    div.tight {
        margin-top: -9px;
        margin-bottom: -9px;
    }
    
    div.button_height {
        font-family: Helvetica;
        font-size: 14px;
        display: inline-block;
        padding-top: 9px;
        padding-bottom: 8px;
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
        #db = Db()
        #sql = "SELECT sum(width) as tableWidth FROM " + Tbl().adderColumns + " ORDER BY srt;"
        #tableWidth = db.getString("tableWidth", sql)

        #cols = self.helper.getNumAdderCols()
        #tableWidth += cols * 4 + 6
        #Services.query(func.sum(Services.price)).filter(Services.dateAdd.between(start, end)).scalar()  # or you can use .scalar() ; .one() ; .first() ; .all() depending on what you want to achieve
        #tableWidth = AdderColumn.query(func.sum(AdderColumn.width)).scalar()
        

        tableWidth = AdderColumn.query.with_entities(func.sum(AdderColumn.width)).first()
        cols = 5
        
        style = self.getCommonStyle() + """
        
    .title_table {
        height: 60px;
        width: """ + str(tableWidth) + """px;
        background-color: #cffffb;
        color: #222222;
        text-align: center;
        border-collapse: collapse;  
        border-top: 1px solid #222222;
        border-left: 1px solid #222222;
        border-right: 1px solid #222222;
        border-bottom: 0px solid #222222;
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

    .fixed_headers tbody td {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 13px;
    }\n"""
    
        adderColumns = AdderColumn.query.order_by(AdderColumn.srt).all()

        c = 1

        for ac in adderColumns:
            style += '    .fixed_headers td:nth-child(' + str(c) + ') {\n'
            style += '        width: ' + str(ac.width) + 'px;\n'
            style += '        text-align: ' + ac.align + ';\n'
            style += '        vertical-align: ' + ac.valign + ';\n'
            style += '    }\n'
            c += 1

           
        style += """
    .fixed_headers thead {
      background-color: #cffffb;
      color: #222222;
    }
    .fixed_headers thead tr {
      display: block;
      position: relative;
    }
    .fixed_headers tbody {
      display: block;
      overflow: auto;
      height: 700px;
    }
    .fixed_headers tbody tr:nth-child(even) {
      background-color: #e0e0e0;
    }
    .active_button {
        background-color: #cffffb;
    }
    .old_ie_wrapper {
      height: 700px;
      width: """ + str(tableWidth)  + """px;
      overflow-x: hidden;
      overflow-y: auto;
    }
    .old_ie_wrapper tbody {
      height: auto;
    }\n"""
            
        return style
   
       
    def getDisplayStyle(self, user):
        #user = User.query.filter(User.login == current_user.login).join(UserColumn).first()

        tableWidth = user.getTableWidth()
        cols = user.getNumCols()
        tableWidth += cols * 4 + 14

        
        style = self.getCommonStyle() + """
        
    div.scrollable {
        width: 100%;
        margin: 0;
        padding: 0;
        overflow: auto;
    }
    
    table.title_table {
        height: 40px;
        width: """ + str(tableWidth) + """px;
        background-color: #cffffb;
        color: #222222;
        vertical-align: center;
        text-align: left;
        border-collapse: collapse;  
        border-top: 1px solid #222222;
        border-left: 1px solid #222222;
        border-right: 1px solid #222222;
        border-bottom: 0px solid #222222;
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
        for col in user.columns:
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
      background-color: #cffffb;
      color: #222222;
    }
    .fixed_headers thead tr {
      display: block;
      position: relative;
    }
    .fixed_headers tbody {
      display: block;
      overflow: auto;
      height: 700px;
    }
    .fixed_headers tbody tr:nth-child(even) {
      background-color: #e0e0e0;
    }
    .old_ie_wrapper {
      height: 700px;
      width: """ + str(tableWidth)  + """px;
      overflow-x: hidden;
      overflow-y: auto;
    }
    .old_ie_wrapper tbody {
      height: auto;
    }\n"""
            
        return style
