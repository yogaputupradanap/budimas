import { watch, ref, onUnmounted } from "vue";
import { enableAnimations } from "./settings";
import anime from "animejs";

export function useToogleClickOutside(
    containerId,
    {
        axis = "translateY",
        easing = "spring(1, 80, 10, 6.5)",
        duration = 1200,
        hideValue = -200,
        showValue = 260,
    } = {},
    { outsideRef = null, setOutsideRef = null } = {}
) {
    const show = ref(true);
    const setShow = (val) => (show.value = val);
    const elementRef = ref(null);

    const trueRef = outsideRef || show;

    const showELement = () => {
        anime({
            targets: elementRef.value,
            [axis]: trueRef.value ? hideValue : showValue,
            opacity: trueRef.value ? 0 : 1,
            duration: !enableAnimations ? 0 : duration,
            easing: easing,
        });
    };

    const checkifClickedOutside = (event) => {
        const current = document.getElementById(containerId);
        if (current && !current.contains(event.target)) {
            setOutsideRef ? setOutsideRef(true) : setShow(true);
        }
    };

    document.addEventListener("mousedown", checkifClickedOutside);

    watch([outsideRef, show], function () {
        showELement();
    });

    onUnmounted(() => {
        document.removeEventListener("mousedown", checkifClickedOutside);
    });

    return [show, elementRef, setShow];
}
