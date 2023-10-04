import type { DialOptions, DialTriggerType } from 'flowbite/lib/esm/components/dial/types';
import { DialInterface } from 'flowbite/lib/esm/components/dial/interface';
declare class Dial implements DialInterface {
    _parentEl: HTMLElement;
    _triggerEl: HTMLElement;
    _targetEl: HTMLElement;
    _options: DialOptions;
    _visible: boolean;
    constructor(parentEl?: HTMLElement | null, triggerEl?: HTMLElement | null, targetEl?: HTMLElement | null, options?: DialOptions);
    _init(): void;
    hide(): void;
    show(): void;
    toggle(): void;
    isHidden(): boolean;
    isVisible(): boolean;
    _getTriggerEventTypes(triggerType: DialTriggerType): {
        showEvents: string[];
        hideEvents: string[];
    };
}
export declare function initDials(): void;
export default Dial;
//# sourceMappingURL=index.d.ts.map