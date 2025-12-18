
/* ==================== UTILITY FUNCTIONS ==================== */

function getCSRFToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta) return meta.getAttribute('content');
  
  // Fallback to cookie method
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === 'csrftoken=') {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
  }
  return cookieValue;
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer') || createToastContainer();
  
  const toast = document.createElement('div');
  toast.className = `px-4 py-3 rounded-lg shadow-lg text-sm font-medium transition-all duration-300 transform translate-x-full opacity-0`;
  
  if (type === 'success') {
    toast.className += ' bg-green-500 text-white';
  } else if (type === 'error') {
    toast.className += ' bg-red-500 text-white';
  } else {
    toast.className += ' bg-blue-500 text-white';
  }
  
  toast.textContent = message;
  container.appendChild(toast);
  
  setTimeout(() => {
    toast.classList.remove('translate-x-full', 'opacity-0');
  }, 10);
  
  setTimeout(() => {
    toast.classList.add('translate-x-full', 'opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

function createToastContainer() {
  const container = document.createElement('div');
  container.id = 'toastContainer';
  container.className = 'fixed top-6 right-6 z-[9999] space-y-3';
  document.body.appendChild(container);
  return container;
}

/* ==================== FOLLOW / UNFOLLOW ==================== */

const activeFollowRequests = new Set();
document.addEventListener('click', async (e) => {
  const btn = e.target.closest('#followBtn');
  if (!btn) return;

  e.preventDefault();
  e.stopPropagation();

  const username = btn.dataset.username;
  const state = btn.dataset.state;
  if (!username || activeFollowRequests.has(username)) return;

  activeFollowRequests.add(username);
  btn.disabled = true;

  const icon = btn.querySelector('#followIcon path');
  const text = btn.querySelector('#followText');

  try {
    const res = await fetch(`/follow/${username}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken(),
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({})
    });

    if (!res.ok) throw new Error();

    const data = await res.json();

    if (data.action === 'followed') {
      btn.dataset.state = 'following';
      text.textContent = 'Unfollow';
      icon.setAttribute(
        'd',
        'M5 13l4 4L19 7'
      );
      showPremiumToast(`Now following ${username}`);
    } else {
      btn.dataset.state = 'not-following';
      text.textContent = 'Follow';
      icon.setAttribute(
        'd',
        'M12 4v16m8-8H4'
      );
      showPremiumToast(`Unfollowed ${username}`);
    }

    // Micro interaction
    btn.animate(
      [{ transform: 'scale(0.95)' }, { transform: 'scale(1)' }],
      { duration: 150, easing: 'ease-out' }
    );

  } catch {
    showPremiumToast('Something went wrong', 'error');
  } finally {
    activeFollowRequests.delete(username);
    btn.disabled = false;
  }
});



/* ==================== REACTIONS (OPTIMIZED) ==================== */

const activeReactionRequests = new Set();

document.addEventListener('click', async (e) => {
  const btn = e.target.closest('.reaction-btn');
  if (!btn) return;

  e.preventDefault();

  const postId = btn.dataset.postId;
  const reactionType = btn.dataset.reaction;
  
  if (!postId || !reactionType) return;

  const requestKey = `${postId}-${reactionType}`;
  if (activeReactionRequests.has(requestKey)) return;

  activeReactionRequests.add(requestKey);

  // Get current state
  const isActive = 
    btn.classList.contains('!text-red-400') || 
    btn.classList.contains('!text-[color:var(--voxa-accent)]') ||
    btn.classList.contains('active');

  // Find all buttons with same reaction
  const allButtons = document.querySelectorAll(
    `.reaction-btn[data-reaction="${reactionType}"][data-post-id="${postId}"]`
  );

  // OPTIMISTIC UI UPDATE
  allButtons.forEach(button => {
    const svg = button.querySelector('svg');
    const countSpan = button.querySelector('.reaction-count');
    
    if (!isActive) {
      // Add active state
      if (reactionType === 'love') {
        button.classList.add('!text-red-400', '!border-red-400/30', '!bg-red-400/5', 'active');
      } else {
        button.classList.add('!text-[color:var(--voxa-accent)]', '!border-[color:var(--voxa-accent)]/30', '!bg-[color:var(--voxa-accent)]/5', 'active');
      }
      if (svg) svg.setAttribute('fill', 'currentColor');
      if (countSpan) {
        const count = parseInt(countSpan.textContent || 0);
        countSpan.textContent = count + 1;
      }
      
      // Animate
      button.style.transform = 'scale(1.15)';
      setTimeout(() => button.style.transform = 'scale(1)', 200);
    } else {
      // Remove active state
      button.classList.remove('!text-red-400', '!border-red-400/30', '!bg-red-400/5',
                            '!text-[color:var(--voxa-accent)]', '!border-[color:var(--voxa-accent)]/30', 
                            '!bg-[color:var(--voxa-accent)]/5', 'active');
      if (svg) svg.setAttribute('fill', 'none');
      if (countSpan) {
        const count = parseInt(countSpan.textContent || 0);
        countSpan.textContent = Math.max(0, count - 1);
      }
    }
  });

  // BACKGROUND SYNC
  try {
    const res = await fetch(`/posts/${postId}/react/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken(),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ reaction: reactionType })
    });

    if (!res.ok) throw new Error("Reaction failed");

    const data = await res.json();

    if (data.success) {
      // Update counts with server response
      allButtons.forEach(button => {
        const countSpan = button.querySelector('.reaction-count');
        if (countSpan && data.count !== undefined) {
          countSpan.textContent = data.count;
        }
      });
    } else {
      throw new Error("Server returned error");
    }

  } catch (err) {
    console.error('Reaction error:', err);
    
    // ROLLBACK on failure
    allButtons.forEach(button => {
      const svg = button.querySelector('svg');
      const countSpan = button.querySelector('.reaction-count');
      
      if (isActive) {
        // Was active, restore active state
        if (reactionType === 'love') {
          button.classList.add('!text-red-400', '!border-red-400/30', '!bg-red-400/5', 'active');
        } else {
          button.classList.add('!text-[color:var(--voxa-accent)]', '!border-[color:var(--voxa-accent)]/30', '!bg-[color:var(--voxa-accent)]/5', 'active');
        }
        if (svg) svg.setAttribute('fill', 'currentColor');
        if (countSpan) {
          const count = parseInt(countSpan.textContent || 0);
          countSpan.textContent = count + 1;
        }
      } else {
        // Was inactive, restore inactive state
        button.classList.remove('!text-red-400', '!border-red-400/30', '!bg-red-400/5',
                              '!text-[color:var(--voxa-accent)]', '!border-[color:var(--voxa-accent)]/30', 
                              '!bg-[color:var(--voxa-accent)]/5', 'active');
        if (svg) svg.setAttribute('fill', 'none');
        if (countSpan) {
          const count = parseInt(countSpan.textContent || 0);
          countSpan.textContent = Math.max(0, count - 1);
        }
      }
    });
    
    showToast('Failed to save reaction. Please try again.', 'error');
  } finally {
    activeReactionRequests.delete(requestKey);
  }
});


/* ==================== COMMENTS (TOP-LEVEL) ==================== */

document.addEventListener('submit', async (e) => {
  const form = e.target.closest('#commentForm');
  if (!form) return;

  e.preventDefault();

  const contentInput = document.getElementById('commentContent');
  const content = contentInput?.value.trim();
  const postId = form.dataset.postId;

  if (!content || !postId) {
    showToast('Please enter a comment', 'error');
    return;
  }

  const submitBtn = form.querySelector('button[type="submit"]');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Posting...';

  try {
    const res = await fetch(`/posts/${postId}/comments/add/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken(),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ content })
    });

    if (!res.ok) throw new Error("Comment failed");

    const data = await res.json();

    if (data.success) {
      showToast('Comment posted successfully!', 'success');
      
      // Update comment count
      const commentCounts = document.querySelectorAll('#commentCountHeader, #commentCountFloating, #commentCountMobile');
      commentCounts.forEach(el => {
        el.textContent = `(${data.comments_count})`;
      });

      // Clear form
      contentInput.value = '';
      
      // Reload to show new comment
      setTimeout(() => location.reload(), 500);
    }

  } catch (err) {
    console.error('Comment error:', err);
    showToast('Failed to post comment. Please try again.', 'error');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Post Comment';
  }
});


/* ==================== REPLY TOGGLE ==================== */

document.addEventListener('click', (e) => {
  const btn = e.target.closest('.reply-btn');
  if (!btn) return;

  const commentId = btn.dataset.commentId;
  if (!commentId) return;

  const container = document.querySelector(
    `.reply-form-container[data-parent-id="${commentId}"]`
  );

  if (container) {
    container.classList.toggle('hidden');
    
    // Focus textarea when opening
    if (!container.classList.contains('hidden')) {
      const textarea = container.querySelector('textarea');
      if (textarea) {
        textarea.focus();
      }
    }
  }
});


/* ==================== REPLY SUBMIT ==================== */

document.addEventListener('submit', async (e) => {
  const form = e.target.closest('.reply-form');
  if (!form) return;

  e.preventDefault();

  const textarea = form.querySelector('textarea');
  const parentInput = form.querySelector('input[name="parent_id"]');

  const content = textarea?.value.trim();
  const parentId = parentInput?.value;

  if (!content || !parentId) {
    showToast('Please enter a reply', 'error');
    return;
  }

  const submitBtn = form.querySelector('button[type="submit"]');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Posting...';

  // Get post ID from the main form
  const mainForm = document.getElementById('commentForm');
  const postId = mainForm?.dataset.postId;

  try {
    const res = await fetch(`/posts/${postId}/comments/add/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken(),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        content,
        parent_id: parentId 
      })
    });

    if (!res.ok) throw new Error("Reply failed");

    const data = await res.json();

    if (data.success) {
      showToast('Reply posted successfully!', 'success');
      
      // Update comment count
      const commentCounts = document.querySelectorAll('#commentCountHeader, #commentCountFloating, #commentCountMobile');
      commentCounts.forEach(el => {
        el.textContent = `(${data.comments_count})`;
      });

      // Clear form and hide
      textarea.value = '';
      form.closest('.reply-form-container')?.classList.add('hidden');
      
      // Reload to show new reply
      setTimeout(() => location.reload(), 500);
    }

  } catch (err) {
    console.error('Reply error:', err);
    showToast('Failed to post reply. Please try again.', 'error');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Reply';
  }
});


/* ==================== DELETE COMMENT / REPLY ==================== */

document.addEventListener('click', async (e) => {
  const btn = e.target.closest('.delete-comment-btn');
  if (!btn) return;

  e.preventDefault();

  if (!confirm("Are you sure you want to delete this comment?")) return;

  const commentId = btn.dataset.commentId;
  if (!commentId) return;

  btn.disabled = true;
  btn.textContent = 'Deleting...';

  try {
    const res = await fetch(`/comments/${commentId}/delete/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken(),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({})
    });

    if (!res.ok) throw new Error("Delete failed");

    const data = await res.json();

    if (data.success) {
      showToast('Comment deleted successfully', 'success');
      
      // Update comment counts
      const commentCounts = document.querySelectorAll('#commentCountHeader, #commentCountFloating, #commentCountMobile');
      commentCounts.forEach(el => {
        el.textContent = `(${data.comments_count})`;
      });

      // Fade out and remove
      const commentItem = btn.closest('.comment-item');
      if (commentItem) {
        commentItem.style.opacity = '0';
        commentItem.style.transform = 'translateX(-20px)';
        commentItem.style.transition = 'all 0.3s ease';
        setTimeout(() => commentItem.remove(), 300);
      }
    }

  } catch (err) {
    console.error('Delete error:', err);
    showToast('Failed to delete comment. Please try again.', 'error');
    btn.disabled = false;
    btn.textContent = 'Delete';
  }
});


/* ==================== SCROLL TO COMMENTS ==================== */

document.addEventListener('DOMContentLoaded', () => {
  // Smooth scroll to comments section
  const commentLinks = document.querySelectorAll('a[href="#comments-section"]');
  commentLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const section = document.getElementById('comments-section');
      if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Focus comment textarea
        setTimeout(() => {
          const textarea = document.getElementById('commentContent');
          if (textarea) textarea.focus();
        }, 500);
      }
    });
  });
});


/* ==================== PERFORMANCE OPTIMIZATION ==================== */

// Lazy load images
if ('IntersectionObserver' in window) {
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          observer.unobserve(img);
        }
      }
    });
  });

  document.querySelectorAll('img[data-src]').forEach(img => {
    imageObserver.observe(img);
  });
}
