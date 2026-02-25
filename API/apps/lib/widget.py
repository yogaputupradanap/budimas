from  .helper  import  *


def btn_details(id, name=None) :
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

def btn_form(id, name=None) :
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

def btn_cetak(id) :
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

def btn_status(status) :
    return f"""<span class="btn btn-sm btn-info pills def-point">{status}</span>"""

def in_checkbox(id, name=None) :
    name = f"-{name}" if not empty(name) else ""
    return f"""
        <div class="form-check">
            <input class="form-check-input in-check{name}" type="checkbox" value="{id}">
        </div>
    """