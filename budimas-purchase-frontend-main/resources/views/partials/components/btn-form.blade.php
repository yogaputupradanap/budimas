<div class='btn-group btn-group-sm' role='group'>
    <button 
        type='button' title='Form' 
        value="{{ $id }}" 
        class='btn btn-form{{ !empty($name) ? "-".$name : "" }} btn-info mx-1'
    ><i class='mdi mdi-receipt mx-1 font-16'></i>
    </button>
</div>