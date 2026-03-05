<div class='btn-group btn-group-sm' role='group'>
    <button 
        type='button' title='Detail' 
        value="{{ $id }}" 
        class='btn btn-detail{{ !empty($name) ? "-".$name : "" }} btn-info mx-1'
    ><i class='mdi mdi-layers mx-1 font-16'></i>
    </button>
</div>