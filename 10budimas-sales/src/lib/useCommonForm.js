/**
 * Custom hook for handling common form operations using vee-validate library.
 * @param {object} schema - The validation schema for the form fields.
 * @param {object} initialValue - The initial values for the form fields.
 * @param {string} validFeedback - The feedback message for successful validation.
 * @returns An object containing functions and properties for form handling.
 */
import { useForm } from "vee-validate";

export function useCommonForm(schema, initialValue, validFeedback) {
  const configProps = (state) => ({
    props: {
      validFeedback: validFeedback ? validFeedback : "validasi sukses",
      invalidFeedback: state.errors[0],
      state: state.errors[0] ? false : state.touched ? true : undefined,
    },
  });

  const { defineField, handleSubmit, resetForm, errors } = useForm({
    validationSchema: schema,
    initialValues: initialValue || null,
  });

  return { defineField, handleSubmit, configProps, resetForm, errors };
}
