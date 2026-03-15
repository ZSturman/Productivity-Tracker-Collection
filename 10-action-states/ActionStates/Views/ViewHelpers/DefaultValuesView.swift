//
//  DefaultValuesView.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/23/23.
//

import SwiftUI
struct DefaultValueNumberView: View {
    @Binding var defaultValueNumber: Double
    
    var body: some View {
        HStack {
            Text("Default: ")
            Spacer()
            TextField("", value: $defaultValueNumber, format: .number)
                .keyboardType(.numbersAndPunctuation)
                .multilineTextAlignment(.trailing)
        }
    }
}
