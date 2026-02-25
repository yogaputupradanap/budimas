from apps.helper import *


def btn_details(id, name=None):
    name = f"-{name}" if not empty(name) else ""
    return f"""
        <div class='btn-group btn-group-sm' role='group'>
            <button 
                type='button' title='Detail' 
                value="{id}" 
                class='btn btn-detail{name} btn-info mx-1'
            ><i class='mdi mdi-layers mx-1 font-16'></i>
            </button>
        </div>
    """


def btn_form(id, name=None):
    name = f"-{name}" if not empty(name) else ""
    return f"""
        <div class='btn-group btn-group-sm' role='group'>
            <button 
                type='button' title='Form' 
                value="{id}" 
                class='btn btn-form{name} btn-info mx-1'
            ><i class='mdi mdi-receipt mx-1 font-16'></i>
            </button>
        </div>
    """


def btn_actions(id, name=None):
    name = f"-{name}" if not empty(name) else ""
    return f"""
        <div class='btn-group btn-group-sm' role='group'>
            <button 
                type='button' title='Edit' 
                value="{id}"
                class='btn btn-edit btn-info mx-1'
            ><i class='mdi mdi-lead-pencil mx-1 font-16'></i>
            </button>
            <button 
                type='button' title='Hapus'  
                value="{id}" 
                class='btn btn-delete btn-danger'
            ><i class='mdi mdi-delete mx-1 font-16'></i>
            </button>
        </div>
    """


def btn_cetak(id):
    return f"""
        <div class='btn-group btn-group-sm' role='group'>
            <button 
                type='button' title='Lihat / Cetak' 
                value="{id}" 
                class='btn btn-print btn-secondary mx-1'
            ><i class='mdi mdi-printer mx-1 font-16'></i>
            </button>
        </div>
    """


def btn_status(status):
    return f"""<span class="btn btn-sm btn-info pills def-point">{status}</span>"""


def create_status_button(text, color):
    """
    Membuat button status dengan warna yang dapat dikustomisasi

    Parameters:
    - text: teks yang akan ditampilkan
    - color: warna button (bootstrap colors: primary, secondary, success, danger, warning, info, light, dark)
    """
    return f"""<span class="btn btn-sm text-white btn-{color} pills def-point">{text}</span>"""


def in_checkbox(id, name=None):
    name = f"-{name}" if not empty(name) else ""
    return f"""
        <div class="form-check">
            <input class="form-check-input in-check{name}" type="checkbox" value="{id}">
        </div>
    """
