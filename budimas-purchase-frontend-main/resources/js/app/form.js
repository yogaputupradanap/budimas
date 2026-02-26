/*
 |--------------------------------------------------------------------------
 | Form Handler.
 |--------------------------------------------------------------------------
 |
 | Global Form Handler Functions & Configurations Collection.
 |
 */
/** 
 * Class of Form Control Handler Collections. 
 * @requires JQuery `$`.
 */
class Forms {
	/**
	 * Initialize Properties and Methods.
	 */
	constructor() {
		this.valid   = true;
		this.el 	 = null; // Element of Form (Optional).
		this.errMsg1 = `<small class="form-error-info">Mohon Lengkapi Data!</small>`;
		this.errMsg2 = `<small class="form-error-info">Format E-mail Tidak Sesuai!</small>`;
	}
    /** 
	 * Memformat `Value` dari Input Money ke Bentuk `Uang`. 
	 * @todo Digunakan saat Selesai Submit/Request Form.
	 */
	setMoneyFormat() {
		// Mencari Input Money.
		let inputs = this.el ? this.el.find(".money") : $(".money");   
		
		// Memformat Value dari Input.
		if (inputs.length > 0) {                             
			inputs.each(function() {                         
				if (!isNull(this.value)) {
					this.value = numberToStr(this.value);    
				}
			});
		}
	}
	/** 
	 * Memformat `Value` dari Input Money ke Bentuk `Angka`. 
	 * @todo Digunakan saat Submit/Request Form.
	 */
	resetMoneyFormat() {
		// Mencari Input Money.
		let inputs = this.el ? this.el.find(".money") : $(".money");   
		
		// Memformat Value dari Input.
		if (inputs.length > 0) {                             
			inputs.each(function() {                         
				if (!isNull(this.value)) {                  
					this.value = strToFloat(this.value);     
				}
			});
		}
	}
	/**
	 * Validation Checker Handler.
	 * @param {number} option 0 : Reset | 1 : Check.
	 */
	validate(option) {
		// Mencari Input, Text Area, dan Select.
		let inputs = this.el 
			? this.el.find('input,textarea,select').filter('[required]') 
			: $('input,textarea,select').filter('[required]');

		if (inputs.length > 0) {
			switch (option) {
				case 0: // Reset Form Validasi.
					inputs.each(function(i, input) {
						// Remove Error Message.
						$(input).closest('.form-group')
								.find('.form-error-info')
								.remove();

						// Remove Form Error Styling Border Class.
						$(input).is('select')
						? $(input).next().find('.select2-selection--single')
								  .removeClass('form-error')
						: $(input).removeClass('form-error');
					});
				break;
				case 1: // Check Form Validasi.
					this.valid = true;
					let instance = this;

					inputs.each(function(i, input) {
						if (isNull(input.value)) {
							// Menandai Jika Form Tidak Valid.
							if (instance.valid == true) { 
								instance.valid = false; 
							}

							// Add Form Error Message.
							$(input).closest('.form-group').find('label')
									.append(instance.errMsg1);

							// Add Form Error Styling Border Class.
							$(input).is('select')
							? $(input).next().find('.select2-selection--single')
									  .addClass('form-error')
							: $(input).addClass('form-error');
						}
					});
				break;
			}
		}
		return this;
	}
	/**
	 * Show Confirmation of a Form Action.
	 */
	confirm() {
		if (this.valid) {
			return Alert().submit();
		}
	}
	/**
	 * Set the Element where Form/Inputs are Located.
	 * @param {object} el Element with JQuery Selector. 
	 */
	set(el) {
		this.el = el;
		return this;
	}
}

// Instantiate Form Class.
var Form = () => { return new Forms(); }