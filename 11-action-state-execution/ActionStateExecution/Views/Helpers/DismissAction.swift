//
//  DismissAction.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/1/23.
//

import SwiftUI

struct DismissAction: ViewModifier {
    @Binding var show: Bool
    var action: () -> Void

    func body(content: Content) -> some View {
        content
            .onReceive(NotificationCenter.default.publisher(for: .init("dismiss"))) { _ in
                show = false
                action()
            }
    }
}

extension View {
    func dismissAction(show: Binding<Bool>, action: @escaping () -> Void) -> some View {
        modifier(DismissAction(show: show, action: action))
    }
}
