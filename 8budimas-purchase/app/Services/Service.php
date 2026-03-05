<?php

namespace App\Services;

class Service 
{
    protected $data; // Data dari Controller.

    /**
     * Menyimpan Data yang Dikirim dari Controller.
     * @param data Illuminate\Http\Request.
     */
    public function setData($data) {
        $this->data = $data;

        // Format Data Null
        foreach($this->data->request as $key => $value) {
            $this->data[$key] = $this->data[$key] ?? ''; 
        }

        return $this;
    }
}