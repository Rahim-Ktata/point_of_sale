//mypreset.ts
import { definePreset } from '@primeuix/themes';
import Material from '@primeuix/themes/material';
import Aura from '@primeuix/themes/aura';
import Lara from '@primeuix/themes/lara';

export const MyPreset = definePreset(Material, {
    //Your customizations, see the following sections for examples
    semantic: {
        typography: {
            lineHeight: '1.5',
            fontFamily: 'Monospace',
            fontWeight: 'normal',
            fontSize: '0.875rem'
        },
        formField: {
            fontWeight: '{typography.font.weight}',
            fontSize: '{typography.font.size}'
        },
    },
    components: {
        
        // select: {
        //     fontSize: '{form.field.font.size}',  // same as formField.fontSize
        //     fontWeight: '{form.field.font.weight}'
        // }
    }
});

// export MyPreset;