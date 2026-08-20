import { describe, it, expect } from 'vitest'
import {
  SECTION_BASE, SECTION_CP, SECTION_BP, ALL_SECTIONS, PUBLISHED_SECTIONS,
  sectionOfTab, visibleSections, isSectionVisible,
} from '~/utils/sections.js'

describe('sectionOfTab', () => {
  it('maps every axis-{id} tab to cp', () => {
    expect(sectionOfTab('axis-1')).toBe(SECTION_CP)
    expect(sectionOfTab('axis-42')).toBe(SECTION_CP)
  })

  it('returns section tabs as-is', () => {
    expect(sectionOfTab(SECTION_BASE)).toBe(SECTION_BASE)
    expect(sectionOfTab(SECTION_CP)).toBe(SECTION_CP)
    expect(sectionOfTab(SECTION_BP)).toBe(SECTION_BP)
  })

  it('returns null for invalid or empty values', () => {
    expect(sectionOfTab('nope')).toBeNull()
    expect(sectionOfTab('')).toBeNull()
    expect(sectionOfTab(null)).toBeNull()
    expect(sectionOfTab(undefined)).toBeNull()
  })
})

describe('visibleSections', () => {
  it('real IES only sees the published sections', () => {
    expect(visibleSections(false)).toEqual(PUBLISHED_SECTIONS)
    expect(visibleSections()).toEqual(PUBLISHED_SECTIONS)
  })

  it('test IES (is_test) sees all sections', () => {
    expect(visibleSections(true)).toEqual(ALL_SECTIONS)
  })
})

describe('isSectionVisible', () => {
  it('cp is hidden for a real IES and visible for a test IES', () => {
    expect(isSectionVisible(SECTION_CP, false)).toBe(false)
    expect(isSectionVisible(SECTION_CP, true)).toBe(true)
  })

  it('published sections are visible for both', () => {
    for (const section of PUBLISHED_SECTIONS) {
      expect(isSectionVisible(section, false)).toBe(true)
      expect(isSectionVisible(section, true)).toBe(true)
    }
  })
})

// La regla que se despliega: la IES real no ve cp, y el fallback de
// [period].vue (default_tab) manda un ?tab= no visible a la primera
// sección publicada.
describe('real IES deep-link rule', () => {
  it('an axis deep-link resolves to cp, which a real IES cannot see', () => {
    const section = sectionOfTab('axis-3')
    expect(section).toBe(SECTION_CP)
    expect(isSectionVisible(section, false)).toBe(false)
  })

  it('the fallback target is the first published section, in order', () => {
    expect(visibleSections(false)[0]).toBe(SECTION_BASE)
  })
})
