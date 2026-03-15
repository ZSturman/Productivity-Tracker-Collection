//
//  InputRowView.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct InputRowView: View {
    @Binding var inputDescription: String
    
    var body: some View {
        TextField("Input Description", text: $inputDescription)
    }
}
