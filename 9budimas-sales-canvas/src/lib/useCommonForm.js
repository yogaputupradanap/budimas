import { useForm } from "vee-validate";

export const useCommonForm = (schema, initialValue, validFeedback) => {
  const configProps = (state) => ({
    props: {
      validFeedback: validFeedback ? validFeedback : "inputan sudah valid",
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
