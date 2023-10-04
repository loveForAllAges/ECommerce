import type { DismissOptions } from 'flowbite/lib/esm/components/dismiss/types';
import { DismissInterface } from 'flowbite/lib/esm/components/dismiss/interface';
declare class Dismiss implements DismissInterface {
    _targetEl: HTMLElement | null;
    _triggerEl: HTMLElement | null;
    _options: DismissOptions;
    constructor(targetEl?: HTMLElement | null, triggerEl?: HTMLElement | null, options?: DismissOptions);
    _init(): void;
    hide(): void;
}
export declare function initDismisses(): void;
export default Dismiss;
//# sourceMappingURL=index.d.ts.map