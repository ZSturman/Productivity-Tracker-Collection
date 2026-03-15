//
//  TriggerOptionsView.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//


import SwiftUI

struct TriggerOptionsView: View {
    @Binding var selectedTriggers: [TriggerType]
    @Environment(\.presentationMode) var presentationMode

    var body: some View {
        List(TriggerType.allCases, id: \.self) { option in
            if !selectedTriggers.contains(option) {
                Button(option.rawValue) {
                    selectedTriggers.append(option)
                    presentationMode.wrappedValue.dismiss()
                }
            } else {
                Text(option.rawValue)
                    .foregroundColor(.gray)
            }
        }
    }
}


enum TriggerType: String, CaseIterable, Identifiable {
    case QuickActionButtonOne = "Quick Action Btn 1"
    case QuickActionButtonTwo = "Quick Action Btn 2"
    case SwipeLeftOne = "Swipe Left One"

    var id: String {
        return self.rawValue
    }
}

