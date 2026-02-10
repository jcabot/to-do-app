import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Tasklist: React.FC = () => {
  return (
    <div id="page-tasklist-1">
    <div id="i94lm" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="i1a9f" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i3cru" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="i1g0b" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="i99hm" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/task">{"Task"}</a>
          <a id="ibj3w" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tasklist">{"TaskList"}</a>
        </div>
        <p id="idq8k" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2025 BESSER. All rights reserved."}</p>
      </nav>
      <main id="iu1re" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="iw60l" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"TaskList"}</h1>
        <p id="ijiws" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage TaskList data"}</p>
        <TableBlock id="table-tasklist-1" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="TaskList List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "ListId", "column_type": "field", "field": "listId", "type": "int", "required": true}, {"label": "Name", "column_type": "field", "field": "name", "type": "str", "required": true}, {"label": "CreatedDate", "column_type": "field", "field": "createdDate", "type": "date", "required": true}, {"label": "Contains", "column_type": "lookup", "path": "contains", "entity": "Task", "field": "taskId", "type": "list", "required": false}], "formColumns": [{"column_type": "field", "field": "listId", "label": "listId", "type": "int", "required": true}, {"column_type": "field", "field": "name", "label": "name", "type": "str", "required": true}, {"column_type": "field", "field": "createdDate", "label": "createdDate", "type": "date", "required": true}, {"column_type": "lookup", "path": "contains", "field": "contains", "lookup_field": "taskId", "entity": "Task", "type": "list", "required": false}]}} dataBinding={{"entity": "TaskList", "endpoint": "/tasklist/"}} />
      </main>
    </div>    </div>
  );
};

export default Tasklist;
