import io
import os
import tarfile

import pandas as pd
import streamlit as st
from PyPDF2 import PdfReader, PdfWriter

page_title = "Apogée Extractor"
st.set_page_config(layout="centered", page_icon="🎓", page_title=page_title)
st.title("🎓 " + page_title)

pdfs = st.file_uploader(
    label="_", label_visibility="collapsed", type="pdf", accept_multiple_files=True
)

dfs = []
readers = {}
if len(pdfs):
    for pdf in pdfs:
        reader = PdfReader(io.BytesIO(pdf.read()))
        dfs.append(
            pd.DataFrame.from_dict(
                {
                    "student": [outline.get("/Title") for outline in reader.outlines],
                    "page": list(range(3, len(reader.outlines) + 3)),
                }
            ).assign(pdf=pdf.name)
        )
        readers[pdf.name] = reader
else:
    st.stop()

df = pd.concat(dfs)

from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column("student", editable=True)
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_side_bar()
grid_options = gb.build()

st.success("💡 Tip! Hold the shift key when selecting rows to select multiple rows at once!")
st.success("💡 Tip! You can edit student names by double-clicking on their names!")
response = AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=False,
)

container = st.empty()
process = container.button("⚙ Process")
if process:
    output_dir = "pdf"
    os.makedirs(output_dir, exist_ok=True)
    for selected_rows in response["selected_rows"]:
        writer = PdfWriter()
        writer.add_page(readers[selected_rows.get("pdf")].pages[selected_rows.get("page") - 1])
        with open(os.path.join(output_dir, selected_rows.get("student") + ".pdf"), "wb") as fp:
            writer.write(fp)
        print(selected_rows)

    tarball = "diploma.tar.gz"
    with tarfile.open(tarball, "w:gz") as tar:
        tar.add(output_dir)

    with open(tarball, "rb") as f:
        container.empty()
        download = container.download_button("⬇ Download", f, file_name=tarball)

    st.success("🎉 Your diploma extraction was generated!")
