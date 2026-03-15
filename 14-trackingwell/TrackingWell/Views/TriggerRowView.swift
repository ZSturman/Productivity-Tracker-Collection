//
//  TriggerRowView.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct TriggerRowView: View {
    @Binding var triggerName: String
    
    var body: some View {
        TextField("Trigger Name", text: $triggerName)
    }
}
