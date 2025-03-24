"""test_app.py"""
from streamlit.testing.v1 import AppTest

# def test_table_to_plot_shape():
#     at = AppTest.from_file("app.py").run(timeout=200)
#     expected_shape = (124, 81)

#     table_to_plot = at.session_state.get("table_to_plot", None)

#     assert at.table_to_plot[0].shape == expected_shape, f"Expected shape {expected_shape}, but got {at.table_to_plot[0].shape}"
