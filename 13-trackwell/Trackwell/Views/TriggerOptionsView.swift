//
//  TriggerOptionsView.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/26/23.
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


//struct TriggerOptionsView_Previews: PreviewProvider {
//    static var previews: some View {
//        TriggerOptionsView()
//    }
//}
