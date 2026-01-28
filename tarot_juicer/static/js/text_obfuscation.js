(function() {
    'use strict';
    
    // Prevent right-click context menu
    const preventContextMenu = (e) => {
        e.preventDefault();
        return false;
    };
    
    // Prevent text selection
    const preventSelection = (e) => {
        e.preventDefault();
        return false;
    };
    
    // Prevent copy action
    const preventCopy = (e) => {
        e.preventDefault();
        e.clipboardData.setData('text/plain', '');
        return false;
    };
    
    // Prevent keyboard shortcuts
    const preventKeyboardShortcuts = (e) => {
        // Prevent Ctrl+C (copy)
        if (e.ctrlKey && e.key === 'c') {
            e.preventDefault();
            return false;
        }
        // Prevent Ctrl+A (select all)
        if (e.ctrlKey && e.key === 'a') {
            e.preventDefault();
            return false;
        }
        // Prevent Ctrl+U (view source)
        if (e.ctrlKey && e.key === 'u') {
            e.preventDefault();
            return false;
        }
        // Prevent Ctrl+S (save page)
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            return false;
        }
        // Prevent F12 (developer tools)
        if (e.key === 'F12') {
            e.preventDefault();
            return false;
        }
        // Prevent Ctrl+Shift+I (developer tools)
        if (e.ctrlKey && e.shiftKey && e.key === 'I') {
            e.preventDefault();
            return false;
        }
        // Prevent Ctrl+Shift+J (console)
        if (e.ctrlKey && e.shiftKey && e.key === 'J') {
            e.preventDefault();
            return false;
        }
        // Prevent Ctrl+Shift+C (inspect element)
        if (e.ctrlKey && e.shiftKey && e.key === 'C') {
            e.preventDefault();
            return false;
        }
    };
    
    // Apply protection to entire main content area
    const applyProtection = () => {
        const mainContainer = document.querySelector('.main-container');
        
        if (mainContainer) {
            // Prevent right-click
            mainContainer.addEventListener('contextmenu', preventContextMenu);
            
            // Prevent selection
            mainContainer.addEventListener('selectstart', preventSelection);
            
            // Prevent drag
            mainContainer.addEventListener('dragstart', preventSelection);
            
            // Prevent copy
            mainContainer.addEventListener('copy', preventCopy);
            
            // Prevent cut
            mainContainer.addEventListener('cut', preventCopy);
        }
        
        // Add keyboard event listeners to document
        document.addEventListener('keydown', preventKeyboardShortcuts);
        
        // Also prevent copy on document level
        document.addEventListener('copy', preventCopy);
        document.addEventListener('cut', preventCopy);
    };
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyProtection);
    } else {
        applyProtection();
    }
    
})();
