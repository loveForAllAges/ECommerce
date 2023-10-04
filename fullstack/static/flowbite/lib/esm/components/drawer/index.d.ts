import type { DrawerOptions, PlacementClasses } from 'flowbite/lib/esm/components/drawer/types';
import { DrawerInterface } from 'flowbite/lib/esm/components/drawer/interface';
declare class Drawer implements DrawerInterface {
    _targetEl: HTMLElement;
    _triggerEl: HTMLElement;
    _options: DrawerOptions;
    _visible: boolean;
    constructor(targetEl?: HTMLElement | null, options?: DrawerOptions);
    _init(): void;
    hide(): void;
    show(): void;
    toggle(): void;
    _createBackdrop(): void;
    _destroyBackdropEl(): void;
    _getPlacementClasses(placement: string): PlacementClasses;
    isHidden(): boolean;
    isVisible(): boolean;
}
export declare function initDrawers(): void;
export default Drawer;
//# sourceMappingURL=index.d.ts.map